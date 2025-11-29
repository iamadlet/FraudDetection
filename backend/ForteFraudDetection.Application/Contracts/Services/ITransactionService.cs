using ForteFraudDetection.Application.Dtos.Json;
using ForteFraudDetection.Application.Dtos.Results;
using System.Security.Claims;

namespace ForteFraudDetection.Application.Contracts.Services
{
    public interface ITransactionService
    {
        Task<string> Send(string recipient, decimal amount, ClaimsPrincipal principal);
        Task<IEnumerable<GetTransactionResult>> GetTransactionsByUser(ClaimsPrincipal principal);
    }
}
