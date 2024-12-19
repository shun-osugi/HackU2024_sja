// UserProfile情報を取得する関数
function getUserProfile() {
    return window.userProfile;
}

// ユーザーがログインしているか確認する関数
function isUserAuthenticated() {
    return window.userProfile.isAuthenticated;
}

// ユーザープロファイルの各フィールドを取得する関数
function getAccountName() {
    if (!window.currentUser || !window.currentUser.isAuthenticated) {
        return null;
    }
    return window.currentUser.username || null;
}

function getDepartment() {
    if (!window.currentUser || !window.currentUser.isAuthenticated) {
        return null;
    }
    return window.currentUser.department || null;
}

function getFaculty() {
    if (!window.currentUser || !window.currentUser.isAuthenticated) {
        return null;
    }
    return window.currentUser.faculty || null;
}

function getGrade() {
    if (!window.currentUser || !window.currentUser.isAuthenticated) {
        return null;
    }
    return window.currentUser.grade || null;
}

// 使用例：
/*
if (isUserAuthenticated()) {
    const profile = getUserProfile();
    console.log(`アカウント名: ${profile.accountName}`);
    console.log(`学部: ${profile.faculty}`);
    console.log(`学科: ${profile.department}`);
    console.log(`学年: ${profile.grade}`);
} else {
    console.log('ログインしていません');
}
*/ 