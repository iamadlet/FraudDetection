namespace ForteFraudDetection.Application.Dtos.Commands
{
    public class SignInCommand
    {
        public string Username { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public string PhoneModel { get; set; } = string.Empty;
        public string OperationalSystem { get; set; } = string.Empty;
    }
}
