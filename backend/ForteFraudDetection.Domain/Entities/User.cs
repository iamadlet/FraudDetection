namespace ForteFraudDetection.Domain.Entities
{
    public class User
    {
        public long Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public ICollection<Session> Sessions { get; set; } = [];
    }
}
