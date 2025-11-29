using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ForteFraudDetection.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddedRecipientConfiguration : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateIndex(
                name: "IX_Transactions_RecipientId",
                table: "Transactions",
                column: "RecipientId");

            migrationBuilder.AddForeignKey(
                name: "FK_Transactions_Users_RecipientId",
                table: "Transactions",
                column: "RecipientId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Transactions_Users_RecipientId",
                table: "Transactions");

            migrationBuilder.DropIndex(
                name: "IX_Transactions_RecipientId",
                table: "Transactions");
        }
    }
}
