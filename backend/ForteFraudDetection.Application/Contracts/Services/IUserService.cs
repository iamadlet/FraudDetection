using ForteFraudDetection.Application.Dtos.Results;
using System.Security.Claims;

namespace ForteFraudDetection.Application.Contracts.Services
{
    public interface IUserService
    {
        Task<SignInResult> SignIn(string name, string password, string phoneModel, string os);
        Task SignUp(string name, string password);
        Task<GetUserResult> GetUserInfo(ClaimsPrincipal principal);
    }
}
