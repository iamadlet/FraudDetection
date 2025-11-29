namespace ForteFraudDetection.Domain.Entities
{
    public class Transaction
    {
        public long Id { get; set; }
        public DateTime DateTime { get; set; }
        public decimal Amount { get; set; }
        public int TransactionNumber { get; set; }
        public long RecipientId { get; set; }
        public User Recipient { get; set; } = null!;
        public long UserId { get; set; }
        public User User { get; set; } = null!;
    }
}
