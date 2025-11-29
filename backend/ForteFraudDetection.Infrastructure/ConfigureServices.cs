using ForteFraudDetection.Application.Common;
using ForteFraudDetection.Application.Contracts.Services;
using ForteFraudDetection.Infrastructure.Persistence;
using ForteFraudDetection.Infrastructure.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.IdentityModel.Tokens;
using System.Text;

namespace ForteFraudDetection.Infrastructure
{
    public static class ConfigureServices
    {
        public static void AddInfrastructureServices(this IServiceCollection services, IConfiguration configuration)
        {
            services.Configure<AppSettings>(configuration);

            var connectionString = configuration.GetConnectionString("DefaultConnection")
                ?? throw new ArgumentNullException("Connection string not found");
            services.AddDbContextPool<AppDbContext>(options => options.UseNpgsql(connectionString));

            services.AddScoped<IUserService, UserService>();
            services.AddScoped<ITransactionService, TransactionService>();
        }
    }
}
