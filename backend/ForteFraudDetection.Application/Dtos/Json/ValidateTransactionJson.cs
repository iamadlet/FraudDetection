using System.Text.Json.Serialization;

namespace ForteFraudDetection.Application.Dtos.Json
{
    public class ValidateTransactionJson
    {
        [JsonPropertyName("transdate")]
        public DateTime TransDate { get; set; }
        [JsonPropertyName("transdatetime")]
        public DateTime TransDateTime { get; set; }
        [JsonPropertyName("amount")]
        public float Amount { get; set; }
        [JsonPropertyName("docno")]
        public int DocNo { get; set; }
        [JsonPropertyName("direction")]
        public string Direction { get; set; } = string.Empty;
        [JsonPropertyName("cst_dim_id")]
        public long CstDimId { get; set; }
    }
}
