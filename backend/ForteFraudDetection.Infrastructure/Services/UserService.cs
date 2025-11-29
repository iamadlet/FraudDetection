using ForteFraudDetection.Application.Common;
using ForteFraudDetection.Application.Contracts.Services;
using ForteFraudDetection.Application.Dtos.Results;
using ForteFraudDetection.Domain.Entities;
using ForteFraudDetection.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace ForteFraudDetection.Infrastructure.Services
{
    public class UserService : IUserService
    {
        private readonly AppDbContext _dbContext;
        private readonly JwtSettings _jwtSettings;

        public UserService(AppDbContext dbContext, IOptions<AppSettings> options) 
        {
            _dbContext = dbContext;
            _jwtSettings = options.Value.Jwt;
        }

        public async Task<SignInResult> SignIn(string name, string password, string phoneModel, string os)
        {
            var user = await _dbContext.Users.FirstOrDefaultAsync(u => u.Name == name && u.Password == password);
            
            if (user == null)
            {
                throw new UnauthorizedAccessException("Invalid username or password.");
            }

            var session = new Session
            {
                UserId = user.Id,
                PhoneModel = phoneModel,
                OperationSystem = os,
                LoginTime = DateTime.UtcNow
            };
            await _dbContext.Sessions.AddAsync(session);
            await _dbContext.SaveChangesAsync();

            return new SignInResult
            {
                Token = await GenerateToken(user, session)
            };
        }

        public async Task SignUp(string name, string password)
        {
            var existingUser = await _dbContext.Users.FirstOrDefaultAsync(u => u.Name == name);

            if (existingUser != null)
                throw new InvalidOperationException("User with the same name already exists.");

            var newUser = new User
            {
                Name = name,
                Password = password
            };

            await _dbContext.Users.AddAsync(newUser);
            await _dbContext.SaveChangesAsync();
        }

        public async Task<GetUserResult> GetUserInfo(ClaimsPrincipal principal)
        {
            var claims = principal.Claims;
            var userIdClaim = claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier)
                ?? throw new UnauthorizedAccessException("Invalid user");
            var userId = long.TryParse(userIdClaim.Value, out var uid) ? uid
                : throw new UnauthorizedAccessException("Invalid user ID");

            var user = await _dbContext.Users
                .FirstOrDefaultAsync(u => u.Id == userId);

            if (user == null)
                throw new KeyNotFoundException("User not found.");

            return new GetUserResult
            {
                Name = user.Name
            };
        }

        private async Task<string> GenerateToken(User user, Session session)
        {
            var claims = new[]
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.Name),
                new Claim(ClaimTypes.Sid, session.Id.ToString())
            };

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwtSettings.Key));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var token = new JwtSecurityToken(
                issuer: _jwtSettings.Issuer,
                audience: _jwtSettings.Audience,
                claims: claims,
                expires: DateTime.Now.AddHours(24),
                signingCredentials: creds);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
