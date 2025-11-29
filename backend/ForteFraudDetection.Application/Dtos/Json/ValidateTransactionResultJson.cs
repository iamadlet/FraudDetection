using System.Text.Json.Serialization;

namespace ForteFraudDetection.Application.Dtos.Json
{
    public class ValidateTransactionResultJson
    {
        public ValidateTransactionResultDataJson Data { get; set; } = new ValidateTransactionResultDataJson();
    }

    public class ValidateTransactionResultDataJson
    {
        [JsonPropertyName("prediction")]
        public int Prediction { get; set; }
        [JsonPropertyName("is_fraud")]
        public bool IsFraud { get; set; }
        [JsonPropertyName("probabilities")]
        public ValidateTransactionResultDataProbabilitiesJson Probabilities { get; set; } = new ValidateTransactionResultDataProbabilitiesJson();
        [JsonPropertyName("timestamp")]
        public string Timestamp { get; set; } = string.Empty;
    }

    public class ValidateTransactionResultDataProbabilitiesJson
    {
        [JsonPropertyName("fraud_probability")]
        public float FraudProbability { get; set; }
        [JsonPropertyName("legitimate_probability")]
        public float LegitimateProbability { get; set; }
    }
}
