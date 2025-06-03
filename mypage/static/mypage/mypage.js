document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.getElementById("edit-btn");
  const saveBtn = document.getElementById("save-btn");
  const profileImg = document.getElementById("profile-img");
  const profileInput = document.getElementById("profile-image-input");
  let isEditing = false;
  let hasUnsavedChanges = false;

  // 프로필 이미지 클릭: 수정 모드일 때만 파일 선택창 열기
  profileImg.addEventListener("click", () => {
    if (!isEditing) return;
    profileInput.click();
  });

  // 파일 선택 후 미리보기
  profileInput.addEventListener("change", () => {
    const file = profileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        profileImg.src = e.target.result;
        hasUnsavedChanges = true;
      };
      reader.readAsDataURL(file);
    }
  });

  // “수정” 버튼 클릭 → 수정 모드 활성화
  editBtn.addEventListener("click", () => {
    toggleEditMode(true);
  });

  // 필드 변경 시 unsaved flag 설정
  const inputs = document.querySelectorAll("input[id$='-input'], textarea[id$='-input']");
  inputs.forEach((el) => {
    el.addEventListener("input", () => {
      if (isEditing) {
        hasUnsavedChanges = true;
      }
    });
  });

  // “저장” 버튼 클릭 → 유효성 검사 + 서버 전송
  saveBtn.addEventListener("click", () => {
    const emailValue = document.getElementById("email-input").value;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(emailValue)) {
      alert("올바른 이메일 형식을 입력해주세요.");
      return;
    }

    const data = {
      nickname: document.getElementById("nickname-input").value,
      email: emailValue,
      location: document.getElementById("location-input").value,
      about: document.getElementById("about-input").value,
      skills: document.getElementById("skills-input").value,
      services: document.getElementById("services-input").value,
    };

    const formData = new FormData();
    formData.append("data", JSON.stringify(data));
    if (profileInput.files && profileInput.files.length > 0) {
      formData.append("profile_image", profileInput.files[0]);
    }

    fetch(`/mypage/update/${USER_ID}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((result) => {
        if (result.success) {
          document.getElementById("nickname-text").textContent = data.nickname;
          document.getElementById("email-text").textContent = data.email;
          document.getElementById("location-text").textContent = data.location;
          document.getElementById("about-text").textContent = data.about;
          document.getElementById("skills-text").textContent = data.skills;
          document.getElementById("services-text").textContent = data.services;
          toggleEditMode(false);
          alert("프로필이 업데이트되었습니다!");
        } else {
          alert("업데이트 실패: " + result.error);
        }
      })
      .catch((err) => {
        console.error("저장 실패:", err);
      });
  });

  // 페이지 이동(새로고침/뒤로가기/링크 클릭 등) 시 경고 띄우기
  window.addEventListener("beforeunload", (e) => {
    if (hasUnsavedChanges) {
      const warningMessage = "변경사항이 저장되지 않았습니다. 정말 이 페이지를 떠나시겠습니까?";
      e.returnValue = warningMessage;
      return warningMessage;
    }
  });

  // 수정 모드 토글 함수
  function toggleEditMode(editing) {
    isEditing = editing;
    hasUnsavedChanges = false; // 모드 전환 시 초기화

    const textElems = document.querySelectorAll("span[id$='-text']");
    const inputElems = document.querySelectorAll("input[id$='-input'], textarea[id$='-input']");

    textElems.forEach((el) => {
      el.style.display = editing ? "none" : "inline";
    });
    inputElems.forEach((el) => {
      el.style.display = editing ? "inline" : "none";
    });

    editBtn.style.display = editing ? "none" : "inline-block";
    saveBtn.style.display = editing ? "inline-block" : "none";

    if (editing) {
      profileImg.classList.add("editing");
      profileImg.style.cursor = "pointer";
      // 수정 모드 진입 시 경고 활성화
      hasUnsavedChanges = true;
    } else {
      profileImg.classList.remove("editing");
      profileImg.style.cursor = "default";
      profileInput.value = "";
      hasUnsavedChanges = false;
    }
  }

  // CSRF 토큰 가져오는 함수 (Django용)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
