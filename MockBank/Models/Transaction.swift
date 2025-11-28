import Foundation

struct Transaction: Identifiable, Decodable {
    var id: UUID = UUID()
    
    var isIncoming: Bool
    var sender: String
    var recipient: String
    var amount: Double
    var date: String
}

struct TransactionResponse: Decodable {
    var isIncoming: Bool
    var dateTime: String
    var amount: Double
    var recipientName: String
    var name: String
}

extension Transaction {
    init(from response: TransactionResponse) {
        self.isIncoming = response.isIncoming
        self.recipient = response.recipientName
        self.sender = response.name
        self.amount = response.amount
        self.date = Transaction.convertDate(from: response.dateTime)
    }
    
    private static func convertDate(from date: String) -> String {
        return String(date.prefix(10))
    }
    
    func formatAmount() -> String {
        return String(format: "$%.2f", amount)
    }
}

extension TransactionResponse {
    func convertDate(from date: String) -> String {
        return String(date.prefix(10))
    }
}

struct SendMoneyRequest: Codable {
    let fromAccount: String
    let toAccount: String
    let amount: Double
}

struct SendMoneyResponse: Decodable {
    let isSuccessful: Bool
    let isFraud: Bool
}

