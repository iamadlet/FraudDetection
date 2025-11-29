import SwiftUI

struct MainView: View {
    @EnvironmentObject private var coordinator: Coordinator
    @StateObject var viewModel: MainViewModel
    
    init(viewModel: MainViewModel) {
        self._viewModel = StateObject(wrappedValue: viewModel)
    }
    
    var body: some View {
        VStack(alignment: .center) {
            // MARK: - Header (welcome text + sign out button)
            HStack {
                VStack(alignment: .leading) {
                    Text("Welcome back,")
                        .foregroundStyle(.secondary)
                    Text(viewModel.username)
                        .font(.system(size: 20, weight: .semibold, design: .rounded))
                }
                
                Spacer()
                
                Button {
                    coordinator.signOut()
                } label: {
                    Image(systemName: "rectangle.portrait.and.arrow.right")
                }
            }
            
            ZStack {
                VStack(alignment: .leading, spacing: 20) {
                    HStack {
                        Image(systemName: "wallet.bifold")
                        Text("Total Balance")
                    }
                    if viewModel.isLoading && viewModel.username.isEmpty {
                        Text("Loading...").redacted(reason: .placeholder)
                    } else {
                        Text("\(viewModel.formatBalance())")
                            .font(.system(size: 25, weight: .semibold, design: .rounded))
                        Text("\(viewModel.username)")
                    }
                }
                .padding(.leading, 16)
                .frame(maxWidth: .infinity, alignment: .leading)
            }
            .frame(height: 170)
            .background(Color.blue)
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .foregroundStyle(Color.white)
            
            HStack {
                CustomButton(coordinator: coordinator, text: "Send Money", username: viewModel.username)
            }
            .padding(.bottom, 16)
            
            HStack {
                Text("Recent Transactions")
                    .font(.system(size: 18, weight: .semibold, design: .rounded))
                Spacer()
                Button {
                    coordinator.push(page: .transactions(username: viewModel.username))
                } label: {
                    HStack {
                        Text("See All")
                            .font(.system(size: 18, weight: .semibold, design: .rounded))
                        Image(systemName: "dollarsign.arrow.trianglehead.counterclockwise.rotate.90")
                    }
                }

            }
            
            ScrollView {
                VStack(spacing: 12) {
                    if viewModel.isLoading {
                        ProgressView()
                            .padding(.top, 100)
                            .scaleEffect(1.5)
                    } else if viewModel.lastThreeTransactions.isEmpty {
                        Text("No transactions yet")
                            .foregroundStyle(.secondary)
                            .padding(.top, 20)
                    } else {
                        ForEach(viewModel.lastThreeTransactions) { transaction in
                            let isIncoming = viewModel.username != transaction.sender
                            TransactionCell(transaction: transaction, isIncoming: isIncoming)
                            
                        }
                    }
                }
            }
            .frame(height: 250)
            Spacer()
        }
        .padding(.horizontal, 16)
        .onAppear {
            viewModel.loadData()
        }
        .refreshable {
            viewModel.loadData()
        }
    }
}

#Preview {
    MainView(viewModel: MainViewModel(transactionService: AppServices.shared.transactionService, authService: AppServices.shared.authService))
}

struct CustomButton: View {
    var coordinator: Coordinator
    var text: String
    var username: String
    var body: some View {
        Button {
            coordinator.presentSheet(.sendFunds(sender: username))
        } label: {
            ZStack {
                RoundedRectangle(cornerRadius: 16).stroke(lineWidth: 1)
                VStack {
                    ZStack {
                        Image(systemName: "arrow.up.forward")
                            .foregroundStyle(.red)
                        Circle().frame(width: 50, height: 50).foregroundColor(.red.opacity(0.4))
                    }
                    Text(text)
                }
            }
            .frame(width: 200, height: 100)
        }

    }
}

struct TransactionCell: View {
    var transaction: Transaction
    var isIncoming: Bool
    var body: some View {
        HStack {
            if !isIncoming {
                ZStack {
                    Image(systemName: "arrow.up.forward")
                        .foregroundStyle(.red)
                    Circle().frame(width: 50, height: 50).foregroundColor(.red.opacity(0.4))
                }
            } else {
                ZStack {
                    Image(systemName: "arrow.down.left")
                        .foregroundStyle(.green)
                    Circle().frame(width: 50, height: 50).foregroundColor(.green.opacity(0.4))
                }
            }
            Spacer()
                .frame(width: 50)
            VStack(alignment: .leading) {
                Text(isIncoming ? transaction.sender : transaction.recipient)
                Text(transaction.date)
            }
            Spacer()
            Text(transaction.formatAmount())
                .foregroundStyle(isIncoming ? .green : .red)
        }
        .padding()
        .background(Color.gray.opacity(0.2))
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}
