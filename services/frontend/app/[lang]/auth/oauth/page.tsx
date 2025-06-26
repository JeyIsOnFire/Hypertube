import styles from "./oauth.module.css"

export default function OAuth() {
    function OAuth42() {
        const id = "u-s4t2ud-2c90b78954c87807b2c6a5381a3d1923e0737de30580e8b2a27f0ee0cdb97460";
        const red = "https://localhost:8443/users/oauth_42/"
        const url = `https://api.intra.42.fr/oauth/authorize?client_id=${id}&redirect_uri=${red}&response_type=code`
        window.location.href = url;
    }

    function OAuthGoogle() {
        const id = "600970262996-1q7dre65rv6msri3e4738n0jmpv3bsfo.apps.googleusercontent.com";
        const red = "https://localhost:8443/users/oauth_google/"
        const url = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${id}&redirect_uri=${red}&response_type=code&scope=openid%20email%20profile&access_type=offline`
        window.location.href = url;
    }

    function OAuthGithub() {
        const id = "Ov23liRq6jwucAzgqs3c";
        const red = "https://localhost:8443/users/oauth_github/"
        const url = `https://github.com/login/oauth/authorize?client_id=${id}&redirect_uri=${red}&scope=user:email`
        window.location.href = url;
    }

    return (
        <div id={styles.oauthMain}>
            <h2 id={styles.title}>Or continue with</h2>
            <button type="button" className={styles.customButton} onClick={OAuth42}>
                <img className={styles.icon} src="/icon_42.png" alt="42 icon" />
                <span>Sign in with 42</span>
            </button>
            <button type="button" className={styles.customButton} onClick={OAuthGoogle}>
                <img className={styles.icon} src="/icon_google.png" alt="google icon" />
                <span>Sign in with Google</span>
            </button>
            <button type="button" className={styles.customButton} onClick={OAuthGithub}>
                <img className={styles.icon} src="/icon_github.png" alt="github icon" />
                <span>Sign in with GitHub</span>
            </button>
        </div>
    )
}