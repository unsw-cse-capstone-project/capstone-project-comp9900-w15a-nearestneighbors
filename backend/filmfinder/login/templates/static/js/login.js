const username = document.getElementById("username");
const password = document.getElementById("password");
const login = document.getElementById("login");

const Invalidusername = document.getElementById("Invalidusername");
const Invalidpassword = document.getElementById("Invalidpassword");
const isValidUserName = () => {
  const pattern = /^.+\@.+\..+$/;
  return pattern.test(username.value);
};

const isValidPassword = () => {
  const pattern = /^.{6,20}$/;
  return pattern.test(password.value);
};

const checkCanSubmit = () => {
  if (isValidPassword() && isValidUserName()) {
    login.removeAttribute("disabled");
  } else {
    login.setAttribute("disabled", "disabled");
  }
};
username.addEventListener("keyup", checkCanSubmit);
password.addEventListener("keyup", checkCanSubmit);

username.addEventListener("blur", () => {
  if (!isValidUserName()) {
    Invalidusername.style.visibility = "visible";
  }
});

username.addEventListener("focus", () => {
  Invalidusername.style.visibility = "hidden";
});

password.addEventListener("blur", () => {
  if (!isValidPassword()) {
    Invalidpassword.style.visibility = "visible";
  }
});

password.addEventListener("focus", () => {
  Invalidpassword.style.visibility = "hidden";
});
