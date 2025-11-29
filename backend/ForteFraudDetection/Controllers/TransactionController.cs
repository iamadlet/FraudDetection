using ForteFraudDetection.Application.Contracts.Services;
using ForteFraudDetection.Application.Dtos.Commands;
using ForteFraudDetection.Controllers.Common;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace ForteFraudDetection.Controllers
{
    [Authorize]
    public class TransactionController : BaseController
    {
        private readonly ITransactionService _transactionService;
        public TransactionController(ITransactionService transactionService)
        {
            _transactionService = transactionService;
        }

        [HttpPost]
        public async Task<IActionResult> Send(SendTransactionCommand command)
        {
            var result = await _transactionService.Send(command.RecipientName, command.Amount, User);
            return Ok(result);
        }

        [HttpGet]
        public async Task<IActionResult> GetAll()
        {
            var transactions = await _transactionService.GetTransactionsByUser(User);
            return Ok(transactions);
        }
    }
}
