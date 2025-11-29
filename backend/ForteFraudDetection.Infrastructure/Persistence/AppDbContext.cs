using ForteFraudDetection.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace ForteFraudDetection.Infrastructure.Persistence
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<Transaction> Transactions { get; set; }
        public DbSet<Session> Sessions { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Name).IsRequired();
                entity.Property(e => e.Password).IsRequired();
                entity.HasMany(e => e.Sessions).WithOne().HasForeignKey(e => e.UserId);
            });
            modelBuilder.Entity<Transaction>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.DateTime).HasConversion(dt => dt, dt => DateTime.SpecifyKind(dt, DateTimeKind.Utc));
                entity.HasOne(e => e.Recipient).WithMany().HasForeignKey(e => e.RecipientId).OnDelete(DeleteBehavior.Restrict);
                entity.HasOne(e => e.User).WithMany().HasForeignKey(e => e.UserId).OnDelete(DeleteBehavior.Restrict);
            });
            modelBuilder.Entity<Session>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.LoginTime).HasConversion(dt => dt, dt => DateTime.SpecifyKind(dt, DateTimeKind.Utc));
            });
        }
    }
}
