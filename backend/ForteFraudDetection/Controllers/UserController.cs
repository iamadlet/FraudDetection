using ForteFraudDetection.Application.Contracts.Services;
using ForteFraudDetection.Application.Dtos.Commands;
using ForteFraudDetection.Controllers.Common;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace ForteFraudDetection.Controllers
{
    public class UserController : BaseController
    {
        private readonly IUserService _userService;

        public UserController(IUserService userService)
        {
            _userService = userService;
        }

        [HttpPost]
        public async Task<IActionResult> SignIn(SignInCommand command)
        {
            var token = await _userService.SignIn(command.Username, command.Password, command.PhoneModel, command.OperationalSystem);
            return Ok(token);
        }

        [HttpPost]
        public async Task<IActionResult> SignUp(SignUpCommand command)
        {
            await _userService.SignUp(command.Username, command.Password);
            return Ok();
        }

        [HttpGet]
        [Authorize]
        public async Task<IActionResult> GetCurrentUser()
        {
            var userInfo = await _userService.GetUserInfo(User);
            return Ok(userInfo);
        }
    }
}
