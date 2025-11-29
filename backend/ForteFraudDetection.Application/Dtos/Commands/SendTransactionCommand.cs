namespace ForteFraudDetection.Application.Dtos.Commands
{
    public class SendTransactionCommand
    {
        public string RecipientName { get; set; } = string.Empty;
        public decimal Amount { get; set; }
    }
}
