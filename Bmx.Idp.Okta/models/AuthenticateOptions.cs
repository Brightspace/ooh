﻿namespace Bmx.Idp.Okta.models {
	public struct AuthenticateOptions {
		public string Username { get; set; }
		public string Password { get; set; }

		public AuthenticateOptions( string username, string password ) {
			Username = username;
			Password = password;
		}
	}
}
