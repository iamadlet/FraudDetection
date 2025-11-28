import SwiftUI

struct SignInView: View {
    @EnvironmentObject private var coordinator: Coordinator
    @StateObject var viewModel: SignInViewModel
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            // MARK: -
            ZStack {
                Image(systemName: "lock")
                    .resizable()
                    .frame(width: 20, height: 25)
                    .foregroundStyle(Color.white)
                
            }
            .padding(20)
            .background(Color.blue)
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .padding(.bottom, 10)
            .frame(maxWidth: .infinity, alignment: .leading)
            
            Text("Welcome Back")
                .font(.system(size: 18))
            
            Text("Sign in to your account")
                .font(.system(size: 18, weight: .regular))
                .foregroundStyle(.secondary)
                .padding(.bottom, 30)
            
            // MARK: - username textfield
            Text("Username")
            TextField("@example", text: $viewModel.username)
                .frame(maxWidth: .infinity)
                .padding(8)
                .background(Color.gray.opacity(0.2))
                .clipShape(RoundedRectangle(cornerRadius: 8))
                .padding(.bottom, 20)
            
            // MARK: - password textfield
            Text("Password")
            SecureField("••••••••", text: $viewModel.password)
                .frame(maxWidth: .infinity)
                .padding(8)
                .background(Color.gray.opacity(0.2))
                .clipShape(RoundedRectangle(cornerRadius: 8))
                .padding(.bottom, 20)
            
            // MARK: - Sign In Button
            Button {
                viewModel.signIn {
                    coordinator.signIn()
                }
            } label: {
                if viewModel.isLoading {
                    ProgressView().tint(.white)
                } else {
                    Text("Sign In")
                        .font(.system(size: 18, weight: .semibold, design: .rounded))
                        .padding(5)
                        .frame(maxWidth: .infinity)
                        .foregroundStyle(Color.white)
                        .background(Color.blue)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                }
            }
            .padding(.bottom, 20)
            
            HStack {
                Text("Don't have an account?")
                Button {
                    ()
                } label: {
                    Text("Sign Up")
                        .fontWeight(.semibold)
                }
            }
            .frame(maxWidth: .infinity)
            
            Spacer()
            

        }
        .padding(.horizontal, 16)
        .alert(isPresented: Binding<Bool>(
            get: { viewModel.errorMessage != nil },
            set: { _ in viewModel.errorMessage = nil }
        )) {
            Alert(
                title: Text("Error"),
                message: Text(viewModel.errorMessage ?? ""),
                dismissButton: .default(Text("OK"))
            )
        }
    }
}

#Preview {
    SignInView(viewModel: SignInViewModel(authService: AppServices.shared.authService))
}
