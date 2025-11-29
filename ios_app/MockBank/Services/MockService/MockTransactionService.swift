import Foundation

import Foundation

final class MockTransactionService: TransactionService {
    
    var shouldSimulateFraud: Bool = false
    
    // MARK: - Mock GetAll (Список транзакций)
    override func getAll(completion: @escaping (Result<[Transaction], Error>) -> Void) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            
            // Создаем фейковые транзакции
            let transactions = [
                Transaction(
                    isIncoming: false,
                    sender: "@adlet",
                    recipient: "Apple Store",
                    amount: 1299.00,
                    date: "2023-11-28"
                ),
                Transaction(
                    isIncoming: true,
                    sender: "Freelance Client",
                    recipient: "@adlet",
                    amount: 500.00,
                    date: "2023-11-27"
                ),
                Transaction(
                    isIncoming: false,
                    sender: "@adlet",
                    recipient: "Starbucks",
                    amount: 12.50,
                    date: "2023-11-26"
                ),
                Transaction(
                    isIncoming: true,
                    sender: "Mom",
                    recipient: "@adlet",
                    amount: 100.00,
                    date: "2023-11-25"
                ),
                Transaction(
                    isIncoming: false,
                    sender: "@adlet",
                    recipient: "Netflix",
                    amount: 15.99,
                    date: "2023-11-24"
                )
            ]
            
            completion(.success(transactions))
        }
    }
    
    override func send(
        requestModel: SendMoneyRequest,
        completion: @escaping (Result<SendMoneyResponse, Error>) -> Void
    ) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            
            if self.shouldSimulateFraud {
                let fraudResponse = SendMoneyResponse(isSuccessful: true, isFraud: true)
                completion(.success(fraudResponse))
            } else {
                let successResponse = SendMoneyResponse(isSuccessful: true, isFraud: false)
                completion(.success(successResponse))
            }
        }
    }
}
