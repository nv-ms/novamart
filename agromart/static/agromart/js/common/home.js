function clearCookies() {
    const cookies = document.cookie.split(';');
    cookies.forEach(cookie => {
        const cookieName = cookie.split('=')[0].trim();
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    });
}
clearCookies()
const csrfToken = "{{ csrf_token }}";
document.cookie = `csrftoken=${csrfToken}; path=/; SameSite=Strict`;