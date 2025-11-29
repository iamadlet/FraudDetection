import SwiftUI

struct TransactionsView: View {
    @EnvironmentObject private var coordinator: Coordinator
    @StateObject var viewModel: TransactionsViewModel
    
    init(viewModel: TransactionsViewModel) {
        self._viewModel = StateObject(wrappedValue: viewModel)
    }
    var body: some View {
        VStack(alignment: .leading) {
            HStack(spacing: 20) {
                Button {
                    coordinator.pop()
                } label: {
                    Image(systemName: "arrow.left")
                }
                .buttonStyle(.plain)
                
                Text("Transaction History")
                    .fontWeight(.semibold)
            }
                
            if viewModel.isLoading {
                Spacer()
                ProgressView()
            } else if let error = viewModel.errorMessage {
                Spacer()
                Text("Ошибка: \(error)")
                Button("Повторить") {
                    viewModel.loadData()
                }
            } else {
                ScrollView {
                    ForEach(viewModel.transactions) { transaction in
                        let isIncoming = viewModel.username != transaction.sender
                        TransactionCell(transaction: transaction, isIncoming: isIncoming)
                    }
                }
            }
        }
        .navigationBarBackButtonHidden()
        .padding(.horizontal)
        .onAppear {
            viewModel.loadData()
        }
        .refreshable {
            viewModel.loadData()
        }
    }
}

#Preview {
    TransactionsView(viewModel: TransactionsViewModel(service: AppServices.shared.transactionService, username: "adlet"))
}
