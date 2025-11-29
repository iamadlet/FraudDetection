import SwiftUI

struct SendFundsView: View {
    @EnvironmentObject private var coordinator: Coordinator
    @StateObject var viewModel: SendFundsViewModel
    var balance: String = "$10000"
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Button {
                    coordinator.dismissSheet()
                } label: {
                    Image(systemName: "xmark")
                        .foregroundStyle(Color.black)
                }
                
                Text("Send Money")
                    .font(.system(size: 20, weight: .semibold, design: .rounded))
            }
            .padding(.top, 30)
            .padding(.bottom, 40)
            
            ZStack {
                VStack(alignment: .leading) {
                    Text("Available Balance")
                        .font(.system(size: 20, weight: .regular))
                    Text(balance)
                        .font(.system(size: 20, weight: .bold, design: .rounded))
                        .foregroundColor(.blue)
                    
                }
                .frame(maxWidth: .infinity, alignment: .leading)
            }
            .padding()
            .background(Color.blue.opacity(0.3))
            .clipShape(RoundedRectangle(cornerRadius: 8))
            .padding(.bottom, 20)
            
            Text("Recipient Name")
                .font(.system(size: 18, weight: .semibold, design: .rounded))
                .padding(.bottom, 8)
            TextField("Enter recipient name", text: $viewModel.recipient)
                .frame(maxWidth: .infinity)
                .padding(8)
                .background(Color.gray.opacity(0.2))
                .clipShape(RoundedRectangle(cornerRadius: 8))
                .padding(.bottom, 20)
            
            Text("Amount")
                .font(.system(size: 18, weight: .semibold, design: .rounded))
                .padding(.bottom, 8)
            TextField("0.00", text: $viewModel.amount)
                .keyboardType(.numberPad)
                .frame(maxWidth: .infinity)
                .padding(8)
                .background(Color.gray.opacity(0.2))
                .clipShape(RoundedRectangle(cornerRadius: 8))
                .padding(.bottom, 20)
            Spacer()
            Button {
                viewModel.sendFunds {
                    print("SUCCESS CLOSURE CALLED")
                    coordinator.dismissSheet()
                }
            } label: {
                Text("Send Money")
                    .font(.system(size: 18, weight: .bold, design: .rounded))
                    .padding(10)
                    .frame(maxWidth: .infinity)
                    .background(Color.blue)
                    .foregroundStyle(Color.white)
                    .cornerRadius(8)
            }
            .padding(.bottom, 24)
            
            Button {
                coordinator.dismissSheet()
            } label: {
                ZStack {
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(lineWidth: 1)
                        .foregroundStyle(Color.black.opacity(0.5))
                    Text("Cancel")
                        .font(.system(size: 18, weight: .bold, design: .rounded))
                        .padding(8)
                        .frame(maxWidth: .infinity)
                        .background(Color.white)
                        .foregroundStyle(Color.black)
                        .cornerRadius(8)
                }
                .frame(height: 10)
            }
            .padding(.bottom, 50)

        }
        .padding(.horizontal, 16)
        .alert("Message", isPresented: Binding<Bool>(
            get: { viewModel.errorMessage != nil },
            set: { _ in viewModel.errorMessage = nil }
        )) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(viewModel.errorMessage ?? "")
        }
    }
}

#Preview {
    SendFundsView(viewModel: SendFundsViewModel(service: AppServices.shared.transactionService))
}
