namespace ForteFraudDetection.Application.Dtos.Results
{
    public class GetTransactionResult
    {
        public bool IsIncoming { get; set; }
        public DateTime DateTime { get; set; }
        public decimal Amount { get; set; }
        public string RecipientName { get; set; } = null!;
        public string Name { get; set; } = null!;
    }
}
