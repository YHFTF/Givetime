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
    signupForm.addEventListener("submit", function (e) {
      e.preventDefault();

      // 기존 에러 메시지 초기화
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
        email.nextElementSibling.textContent = "이메일을 입력해주세요.";
        valid = false;
      } else if (!emailPattern.test(email.value)) {
        email.nextElementSibling.textContent =
          "올바른 이메일 형식을 입력해주세요. (예: user@example.com)";
        valid = false;
      }

      // 닉네임 검사
      if (!nickname.value.trim()) {
        nickname.nextElementSibling.textContent = "닉네임을 입력해주세요.";
        valid = false;
      } else if (nickname.value.trim().length < 2) {
        nickname.nextElementSibling.textContent =
          "닉네임은 2자 이상이어야 합니다.";
        valid = false;
      } else if (nickname.value.trim().length > 20) {
        nickname.nextElementSibling.textContent =
          "닉네임은 20자 이하여야 합니다.";
        valid = false;
      }

      // 비밀번호 검사
      if (!password1.value) {
        password1.nextElementSibling.textContent =
          "비밀번호를 영문과 숫자를 포함하여 8자 이상 입력해주세요.";
        valid = false;
      } else if (password1.value.length < 8) {
        password1.nextElementSibling.textContent =
          "비밀번호는 8자 이상이어야 합니다.";
        valid = false;
      } else if (!/(?=.*[a-zA-Z])(?=.*\d)/.test(password1.value)) {
        password1.nextElementSibling.textContent =
          "비밀번호는 영문과 숫자를 포함해야 합니다.";
        valid = false;
      }

      // 비밀번호 확인
      if (!password2.value) {
        password2.nextElementSibling.textContent =
          "비밀번호 확인을 입력해주세요.";
        valid = false;
      } else if (password1.value !== password2.value) {
        password2.nextElementSibling.textContent =
          "비밀번호가 일치하지 않습니다.";
        valid = false;
      }

      // 거주지 검사
      if (!location.value.trim()) {
        location.nextElementSibling.textContent = "거주지를 입력해주세요.";
        valid = false;
      }

      if (!valid) {
        return; // 오류가 있으면 서버 요청 안함
      }

      const formData = new FormData(signupForm);
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      // 로딩 상태 표시
      const submitButton = signupForm.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;
      submitButton.textContent = "회원가입 중...";
      submitButton.disabled = true;

      fetch("/account/signup/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        body: formData,
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            // 🔥 성공 시 처리 수정
            alert(
              "🎉 회원가입이 완료되었습니다!\n로그인 후 서비스를 이용해주세요."
            );
            closeSignupModal();
            signupForm.reset(); // 폼 초기화
            // 로그인 모달 자동 열기
            openLoginModal();
          } else {
            // 실패 시 서버 에러 메시지 표시
            alert(
              data.message || "회원가입에 실패했습니다. 입력값을 확인해주세요."
            );
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("회원가입 중 오류가 발생했습니다.");
        })
        .finally(() => {
          // 버튼 상태 복원
          submitButton.textContent = originalText;
          submitButton.disabled = false;
        });
    });
  }

  // ✅ 로그인 모달 Ajax 요청 (기존 폼 구조에 맞춤)
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
              alert("🎉 " + (data.message || "로그인에 성공했습니다!"));
              closeLoginModal();
              loginForm.reset(); // 폼 초기화

              // 페이지 새로고침
              window.location.reload();
            } else {
              // 로그인 실패
              alert("❌ " + (data.message || "로그인에 실패했습니다."));
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("로그인 중 오류가 발생했습니다.");
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
        alert(data.message);
        window.location.href = data.redirect_url;
      })
      .catch((err) => {
        console.error("로그아웃 에러:", err);
        alert("로그아웃 중 오류가 발생했습니다.");
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

