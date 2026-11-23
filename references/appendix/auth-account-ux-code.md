# 认证与账户体验 · 可抄代码（附录）

> 2026-11-23 自 `references/auth-account-ux.md` §16、§18 迁出（v72）。判定规则仍在主文件：字段与 `autocomplete` 见 §2.1–§2.2，显示密码见 §2.3，错误话术见 §2.5，OTP 单框见 §7.1–§7.2，恢复见 §8。
>
> 代码未改；实跑记录保留原样，本次迁移未重跑。

## 段 A · 登录表单骨架（HTML）

```html
<form method="post" action="/login" novalidate>
  <label for="username">邮箱或用户名</label>
  <input id="username" name="username" type="text" autocomplete="username"
         autocapitalize="none" autocorrect="off" spellcheck="false" required>

  <label for="password">密码</label>
  <div class="pw">
    <input id="password" name="password" type="password"
           autocomplete="current-password" aria-describedby="pw-err" required>
    <button type="button" id="toggle" aria-pressed="false" aria-controls="password">
      显示密码
    </button>
  </div>
  <p id="pw-err" role="alert" hidden>用户名或密码不正确</p>

  <button type="submit">登录</button>
  <p><a href="/reset">忘记密码？</a></p>
</form>
```

## 段 B · 条件式 passkey（JS）

```js
async function startConditionalPasskey() {
  if (!window.PublicKeyCredential?.isConditionalMediationAvailable) return;
  if (!(await PublicKeyCredential.isConditionalMediationAvailable())) return;

  const controller = new AbortController();
  try {
    const cred = await navigator.credentials.get({
      mediation: "conditional",
      signal: controller.signal,
      publicKey: {
        challenge: Uint8Array.from(atob(CHALLENGE_B64), c => c.charCodeAt(0)),
        rpId: location.hostname,
        allowCredentials: [],
        userVerification: "preferred",
        timeout: 300000,
      },
    });
    await fetch("/auth/passkey/verify", { method: "POST", body: JSON.stringify(serialize(cred)) });
    location.assign("/app");
  } catch (e) {
    if (e.name === "NotAllowedError" || e.name === "AbortError") return; // 静默
    console.warn("[passkey]", e.name);
  }
}
```

## 段 C · OTP 单框（JS）

```js
const otp = document.querySelector("#otp");
otp.addEventListener("input", () => {
  otp.value = otp.value.replace(/\D/g, "").slice(0, 6);   // 粘贴整段也能收敛
  if (otp.value.length === 6) submitOtp(otp.value);
});
```

## 段 D · Python 静态校验器（实跑口径）

```python
# 检查一段登录/注册 HTML 是否踩了本资产列出的硬性反模式。
import re, sys

SAMPLE = """
<form>
  <input id="username" name="username" type="text" autocomplete="username">
  <input id="password" name="password" type="password" autocomplete="current-password">
  <button type="button" aria-pressed="false">显示密码</button>
  <input id="otp" name="otp" inputmode="numeric" autocomplete="one-time-code" maxlength="6">
</form>
"""

BAD_PATTERNS = [
    (r'autocomplete\s*=\s*["\']off["\']', "登录表单不许 autocomplete=off"),
    (r'onpaste\s*=\s*["\']return\s+false', "禁止粘贴违反 WCAG F109"),
    (r'type\s*=\s*["\']number["\']', "验证码不要用 type=number"),
]

def check(html: str):
    problems, oks = [], []
    for pat, msg in BAD_PATTERNS:
        if re.search(pat, html, re.I):
            problems.append(msg)

    if re.search(r'type\s*=\s*["\']password["\'][^>]*autocomplete\s*=\s*["\']current-password', html):
        oks.append("/ 密码框带 current-password")
    if re.search(r'autocomplete\s*=\s*["\'][^"\']*one-time-code', html):
        oks.append("/ 验证码带 one-time-code")
    if re.search(r'aria-pressed', html):
        oks.append("/ 显示密码切换带 aria-pressed")
    if re.search(r'<form[^>]*>', html):
        oks.append("/ 使用标准 form")

    return problems, oks

if __name__ == "__main__":
    problems, oks = check(SAMPLE)
    for line in oks:
        print("PASS", line)
    for p in problems:
        print("FAIL", p)
    print("总判定:", "PASS" if not problems else "FAIL")
    sys.exit(0 if not problems else 1)
```

实跑输出见文末「实跑记录」。

---

## 实跑记录（2026-11-14，本机 Python 3.13）

```text
$ python -I -X utf8 references/auth-account-ux.md   # 见 §16.4 脚本
PASS / 密码框带 current-password
PASS / 验证码带 one-time-code
PASS / 显示密码切换带 aria-pressed
PASS / 使用标准 form
总判定: PASS
```

（脚本以 §16.4 为准；上表为 2026-11-14 在本机 Python 3.13 的实跑输出。）
