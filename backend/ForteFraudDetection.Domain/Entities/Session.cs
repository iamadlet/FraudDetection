namespace ForteFraudDetection.Domain.Entities
{
    public class Session
    {
        public long Id { get; set; }
        public DateTime LoginTime { get; set; }
        public string PhoneModel { get; set; } = string.Empty;
        public string OperationSystem { get; set; } = string.Empty;
        public long UserId { get; set; }
    }
}
