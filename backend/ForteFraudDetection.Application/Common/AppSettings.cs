namespace ForteFraudDetection.Application.Common
{
    public class AppSettings
    {
        public JwtSettings Jwt { get; set; } = null!;
        public PythonProjectSettings PythonProject { get; set; } = null!;
    }

    public class JwtSettings
    {
        public string Issuer { get; set; } = string.Empty;
        public string Audience { get; set; } = string.Empty;
        public string Key { get; set; } = string.Empty;
    }

    public class PythonProjectSettings
    {
        public string BaseUrl { get; set; } = string.Empty;
        public string CreateValidatedTransaction { get; set; } = string.Empty;
        public string CreatePattern { get; set; } = string.Empty;
        public string ValidateTransaction { get; set; } = string.Empty;
        public string TriggerRetraining { get; set; } = string.Empty;
    }
}
