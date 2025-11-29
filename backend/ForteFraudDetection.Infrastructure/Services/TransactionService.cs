using ForteFraudDetection.Application.Common;
using ForteFraudDetection.Application.Contracts.Services;
using ForteFraudDetection.Application.Dtos.Json;
using ForteFraudDetection.Application.Dtos.Results;
using ForteFraudDetection.Domain.Entities;
using ForteFraudDetection.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using System.Buffers.Text;
using System.Net.Http.Headers;
using System.Security.Claims;
using System.Text;
using System.Text.Json;

namespace ForteFraudDetection.Infrastructure.Services
{
    public class TransactionService : ITransactionService
    {
        private readonly AppDbContext _dbContext;
        private readonly HttpClient _httpClient;
        private readonly PythonProjectSettings _pythonProject;

        public TransactionService(AppDbContext appDbContext, IOptions<AppSettings> options)
        {
            _dbContext = appDbContext;
            _pythonProject = options.Value.PythonProject;
            _httpClient = new HttpClient();

        }

        public async Task<string> Send(string recipient, decimal amount, ClaimsPrincipal principal)
        {
            var claims = principal.Claims;
            var userIdClaim = claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier)
                ?? throw new UnauthorizedAccessException("Invalid user");
            var sessionIdClaim = claims.FirstOrDefault(c => c.Type == ClaimTypes.Sid)
                ?? throw new UnauthorizedAccessException("Invalid session");

            var userId = long.TryParse(userIdClaim.Value, out var uid) ? uid
                : throw new UnauthorizedAccessException("Invalid user ID");
            var sessionId = long.TryParse(sessionIdClaim.Value, out var sid) ? sid
                : throw new UnauthorizedAccessException("Invalid session ID");

            if (_dbContext.Users.FirstOrDefault(u => u.Id == userId) == null)
                throw new UnauthorizedAccessException("User not found");
            if (_dbContext.Sessions.FirstOrDefault(s => s.Id == sessionId && s.UserId == userId) == null)
                throw new UnauthorizedAccessException("Session not found");

            var transactionCount = _dbContext.Transactions.Count(t => t.UserId == userId);
            var recipientUser = await _dbContext.Users.FirstOrDefaultAsync(u => u.Name == recipient)
                ?? throw new ArgumentNullException("Recipient not found");

            var transaction = new Transaction
            {
                RecipientId = recipientUser.Id,
                Amount = amount,
                TransactionNumber = transactionCount + 1,
                UserId = userId,
                DateTime = DateTime.UtcNow
            };

            _httpClient.BaseAddress = new Uri(_pythonProject.BaseUrl);
            var direction = Convert.ToBase64String(BitConverter.GetBytes(transaction.RecipientId));
            var transactionModel = new ValidateTransactionJson
            {
                Amount = float.Parse(transaction.Amount.ToString()),
                CstDimId = transaction.UserId,
                DocNo = transaction.TransactionNumber,
                TransDate = transaction.DateTime.Date,
                TransDateTime = transaction.DateTime,
                Direction = direction
            };

            var transactionJson = JsonSerializer.Serialize(transactionModel);
            Console.WriteLine(transactionJson);
            var stringContent = new StringContent(transactionJson);
            stringContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");
            var response = await _httpClient.PostAsync(_pythonProject.ValidateTransaction, stringContent);

            var responseText = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseText);

            if (!response.IsSuccessStatusCode)
            {
                throw new InvalidOperationException("Response invalid");
            }

            await _dbContext.Transactions.AddAsync(transaction);
            await _dbContext.SaveChangesAsync();

            return responseText;
        }

        public async Task<IEnumerable<GetTransactionResult>> GetTransactionsByUser(ClaimsPrincipal principal)
        {
            var claims = principal.Claims;
            var userIdClaim = claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier)
                ?? throw new UnauthorizedAccessException("Invalid user");
            var userId = long.TryParse(userIdClaim.Value, out var uid) ? uid
                : throw new UnauthorizedAccessException("Invalid user ID");

            var identityName = principal.Identity?.Name
                ?? throw new UnauthorizedAccessException("Identity name not provided");

            var transactions = await _dbContext.Transactions.Include(t => t.Recipient).Include(t => t.User).Where(u => u.UserId == userId || u.RecipientId == userId).OrderByDescending(t => t.DateTime).ToListAsync();

            return transactions.Select(t => new GetTransactionResult()
            {
                Amount = t.Amount,
                DateTime = t.DateTime,
                RecipientName = t.Recipient.Name,
                Name = t.User.Name,
                IsIncoming = identityName == t.Recipient.Name
            });
        }
    }
}
