function getCookie(name) {
  let cookieValue = null;
  if (document.cookie) {
    document.cookie.split(";").forEach((cookie) => {
      let [key, val] = cookie.trim().split("=");
      if (key === name) cookieValue = decodeURIComponent(val);
    });
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
  // ✅ 슬라이드 코드
  const wrapper = document.getElementById("slideWrapper");
  if (wrapper) {
    const slides = Array.from(wrapper.children);
    const slideCount = slides.length;
    const firstClone = slides[0].cloneNode(true);
    wrapper.appendChild(firstClone);
    let index = 0;

    setInterval(() => {
      index++;
      wrapper.style.transition = "transform 1s ease-in-out";
      wrapper.style.transform = `translateX(-${index * 100}%)`;

      if (index === slideCount) {
        setTimeout(() => {
          wrapper.style.transition = "none";
          wrapper.style.transform = "translateX(0%)";
          index = 0;
        }, 1000);
      }
    }, 4000);
  }

  // ✅ 회원가입 모달 Ajax 요청
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      // 에러 메시지 초기화
      const errorMessages = signupForm.querySelectorAll(".error-message");
      errorMessages.forEach((span) => (span.textContent = ""));

      let valid = true;

      const email = signupForm.querySelector('input[name="email"]');
      const nickname = signupForm.querySelector('input[name="nickname"]');
      const password1 = signupForm.querySelector('input[name="password1"]');
      const password2 = signupForm.querySelector('input[name="password2"]');
      const location = signupForm.querySelector('input[name="location"]');

      // 이메일 검사
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email.value.trim()) {
        setErrorMessage(email, "이메일을 입력해주세요.");
        valid = false;
      } else if (!emailPattern.test(email.value)) {
        setErrorMessage(
          email,
          "올바른 이메일 형식을 입력해주세요. (예: user@example.com)"
        );
        valid = false;
      }

      // 닉네임 검사
      if (!nickname.value.trim()) {
        setErrorMessage(nickname, "닉네임을 입력해주세요.");
        valid = false;
      } else if (nickname.value.trim().length < 2) {
        setErrorMessage(nickname, "닉네임은 2자 이상이어야 합니다.");
        valid = false;
      } else if (nickname.value.trim().length > 20) {
        setErrorMessage(nickname, "닉네임은 20자 이하여야 합니다.");
        valid = false;
      }

      // 닉네임 중복 검사 (기본 유효성 통과 후 실행)
      if (valid) {
        const nicknameCheck = await checkNicknameDuplicate(nickname);
        if (!nicknameCheck) {
          valid = false;
        }
      }

      // 비밀번호 검사
      if (!password1.value) {
        setErrorMessage(
          password1,
          "비밀번호를 영문과 숫자를 포함하여 8자 이상 입력해주세요."
        );
        valid = false;
      } else if (password1.value.length < 8) {
        setErrorMessage(password1, "비밀번호는 8자 이상이어야 합니다.");
        valid = false;
      } else if (!/(?=.*[a-zA-Z])(?=.*\d)/.test(password1.value)) {
        setErrorMessage(password1, "비밀번호는 영문과 숫자를 포함해야 합니다.");
        valid = false;
      }

      // 비밀번호 확인
      if (!password2.value) {
        setErrorMessage(password2, "비밀번호 확인을 입력해주세요.");
        valid = false;
      } else if (password1.value !== password2.value) {
        setErrorMessage(password2, "비밀번호가 일치하지 않습니다.");
        valid = false;
      }

      // 거주지 검사
      if (!location.value.trim()) {
        setErrorMessage(location, "거주지를 입력해주세요.");
        valid = false;
      }

      if (!valid) return; // 유효성 통과 못하면 종료

      async function checkNicknameDuplicate(nicknameInput) {
        const nick = nicknameInput.value.trim();
        try {
          const response = await fetch(
            `/account/check-nickname/?nickname=${encodeURIComponent(nick)}`
          );
          const data = await response.json();
          if (data.exists) {
            setErrorMessage(nicknameInput, "이미 사용 중인 닉네임입니다.");
            return false;
          } else {
            setErrorMessage(nicknameInput, "");
            return true;
          }
        } catch (error) {
          console.error("닉네임 확인 오류:", error);
          setErrorMessage(nicknameInput, "중복 확인 중 오류가 발생했습니다.");
          return false;
        }
      }

      const formData = new FormData(signupForm);
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;
      const submitButton = signupForm.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;

      submitButton.textContent = "회원가입 중...";
      submitButton.disabled = true;

      fetch("/account/signup/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            showPopup("🎉 회원가입에 성공했습니다. 로그인 후 이용해주세요");
            closeSignupModal();
            signupForm.reset();
            openLoginModal();
          } else {
            sessionStorage.setItem(
              "popupMessage",
              data.message || "회원가입에 실패했습니다. 입력창을 확인해주세요"
            );
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          showPopup("회원가입 중 오류가 발생했습니다.");
        })
        .finally(() => {
          submitButton.textContent = originalText;
          submitButton.disabled = false;
        });
    });
  }

  const loginModal = document.getElementById("loginModal");
  if (loginModal) {
    const loginForm = loginModal.querySelector("form");
    if (loginForm) {
      loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(loginForm);
        const csrfToken = loginForm.querySelector(
          'input[name="csrfmiddlewaretoken"]'
        ).value;

        // 로딩 상태 표시
        const submitButton = loginForm.querySelector(".login-btn");
        const originalText = submitButton.textContent;
        submitButton.textContent = "로그인 중...";
        submitButton.disabled = true;

        fetch("/account/login/", {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: formData,
        })
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            if (data.success) {
              // 로그인 성공
              closeLoginModal();
              sessionStorage.setItem(
                "popupMessage",
                data.message || "로그인에 성공했습니다!"
              );
              // 페이지 새로고침
              window.location.reload();
            } else {
              // 로그인 실패
              sessionStorage.setItem(
                "popupMessage",
                data.message || "로그인에 실패했습니다! 이메일 또는 비밀번호를 다시 입력해주세요."
              );
              showPopup("로그인에 실패했습니다! 이메일 또는 비밀번호를 다시 입력해주세요.");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            sessionStorage.setItem(
              "popupMessage",
              "로그인 중 오류가 발생했습니다."
            );
            showPopup("로그인 중 오류가 발생했습니다.");
          })
          .finally(() => {
            // 버튼 상태 복원
            submitButton.textContent = originalText;
            submitButton.disabled = false;
          });
      });
    }
  }
  const logoutBtn = document.getElementById("logoutBtn");
  if (!logoutBtn) return;

  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    .split("=")[1];
  const logoutUrl = document.querySelector('meta[name="logout-url"]').content;

  logoutBtn.addEventListener("click", (e) => {
    e.preventDefault();
    fetch(logoutUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        window.location.href = data.redirect_url;
        sessionStorage.setItem("popupMessage", data.message || "");
      })
      .catch((err) => {
        console.error("로그아웃 에러:", err);
        sessionStorage.setItem(
          "popupMessage",
          "로그아웃 중 오류가 발생했습니다."
        );
      });
  });
});

// ✅ 로그인 모달 열고 닫기
function openLoginModal() {
  document.getElementById("loginModal").style.display = "flex";
  document.getElementById("signupModal").style.display = "none";

  // 폼 초기화
  const loginForm = document.getElementById("loginModal").querySelector("form");
  if (loginForm) {
    loginForm.reset();
    const errorMessages = loginForm.querySelectorAll(".error-message");
    errorMessages.forEach((span) => (span.textContent = ""));
  }
}

function closeLoginModal() {
  document.getElementById("loginModal").style.display = "none";
}

// ✅ 회원가입 모달 열고 닫기
function openSignupModal() {
  document.getElementById("signupModal").style.display = "flex";
  document.getElementById("loginModal").style.display = "none";

  // 폼 초기화
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.reset();
    const errorMessages = signupForm.querySelectorAll(".error-message");
    errorMessages.forEach((span) => (span.textContent = ""));
  }
}

function closeSignupModal() {
  document.getElementById("signupModal").style.display = "none";
}

// ✅ 비밀번호 토글 (기존 함수명과 매개변수 맞춤)
function togglePassword(inputId) {
  const pwd = document.getElementById(inputId);
  const toggleButton = pwd.parentElement.querySelector('button[type="button"]');

  if (pwd.type === "password") {
    pwd.type = "text";
    if (toggleButton) toggleButton.textContent = "🙈";
  } else {
    pwd.type = "password";
    if (toggleButton) toggleButton.textContent = "👁️";
  }
}

// ✅ 모달 외부 클릭시 닫기
document.addEventListener("click", function (e) {
  const loginModal = document.getElementById("loginModal");
  const signupModal = document.getElementById("signupModal");

  if (e.target === loginModal) {
    closeLoginModal();
  }

  if (e.target === signupModal) {
    closeSignupModal();
  }
});

// ✅ ESC 키로 모달 닫기
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeLoginModal();
    closeSignupModal();
  }
});

function setErrorMessage(input, message) {
  const errorSpan = input.parentElement.querySelector(".error-message");
  const helpText = input.parentElement.querySelector(".help-text");

  if (errorSpan) errorSpan.textContent = message;
  if (helpText) helpText.style.display = message ? "none" : "block";
}