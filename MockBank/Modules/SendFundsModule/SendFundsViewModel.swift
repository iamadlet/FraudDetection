import Foundation

final class SendFundsViewModel: ObservableObject {
    @Published var sender: String = ""
    @Published var recipient: String = ""
    @Published var amount: String = ""
    
    @Published var isLoading: Bool = false
    @Published var errorMessage: String? = nil
    
    private let service: TransactionService
    
    init(service: TransactionService) {
        self.service = service
    }
    
    func sendFunds(onSuccess: @escaping () -> Void) {
        errorMessage = nil
        
        guard !recipient.isEmpty else {
            errorMessage = "Please enter a recipient name."
            return
        }
        
        let cleanAmount = amount.replacingOccurrences(of: ",", with: ".")
        guard let amountValue = Double(cleanAmount), amountValue > 0 else {
            errorMessage = "Please enter a valid amount greater than 0."
            return
        }
        
        isLoading = true
        let request = SendMoneyRequest(fromAccount: sender, toAccount: recipient, amount: amountValue)
        
        service.send(requestModel: request) { [weak self] result in
            DispatchQueue.main.async {
                self?.isLoading = false
                
                switch result {
                case .success(let response):
                    if response.isFraud == true {
                        self?.errorMessage = "Transaction declined: Fraud suspected! Contact support."
                    } else {
                        onSuccess()
                    }
                case .failure(let error):
                    self?.errorMessage = error.localizedDescription
                }
            }
        }
    }
}
