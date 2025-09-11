// Password Strength Indicator
class PasswordStrengthIndicator {
    constructor(passwordFieldId, confirmPasswordFieldId = null) {
        this.passwordField = document.getElementById(passwordFieldId);
        this.confirmPasswordField = confirmPasswordFieldId ? document.getElementById(confirmPasswordFieldId) : null;
        
        if (this.passwordField) {
            this.init();
        }
    }

    init() {
        this.createStrengthIndicator();
        if (this.confirmPasswordField) {
            this.createPasswordMatchIndicator();
        }

        this.passwordField.addEventListener('input', () => {
            this.updateStrengthIndicator();
        });

        if (this.confirmPasswordField) {
            this.confirmPasswordField.addEventListener('input', () => {
                this.updatePasswordMatchIndicator();
            });
        }
    }

    createStrengthIndicator() {
        const strengthContainer = document.createElement('div');
        strengthContainer.className = 'password-strength-container';
        strengthContainer.innerHTML = `
            <div class="password-strength-bar">
                <div class="password-strength-fill" id="strength-fill"></div>
            </div>
            <div class="password-strength-text" id="strength-text">
                <span class="strength-label">Password Strength</span>
                <span class="strength-status">Weak </span>
            </div>
            <div class="password-requirements" id="password-requirements">
                <div class="requirement" id="req-length">
                    <span class="req-icon">❌</span> At least 8 characters
                </div>
                <div class="requirement" id="req-uppercase">
                    <span class="req-icon">❌</span> At least one uppercase letter
                </div>
                <div class="requirement" id="req-number">
                    <span class="req-icon">❌</span> At least one number
                </div>
                <div class="requirement" id="req-symbol">
                    <span class="req-icon">❌</span> At least one symbol
                </div>
            </div>
        `;

        this.passwordField.parentNode.insertBefore(strengthContainer, this.passwordField.nextSibling);
        
        this.strengthFill = document.getElementById('strength-fill');
        this.strengthText = document.getElementById('strength-text');
        this.requirements = document.getElementById('password-requirements');
    }

    createPasswordMatchIndicator() {
        const matchContainer = document.createElement('div');
        matchContainer.className = 'password-match-container';
        matchContainer.innerHTML = `
            <div class="password-match-text" id="password-match-text">
                <span class="match-status"></span>
            </div>
        `;

        this.confirmPasswordField.parentNode.insertBefore(matchContainer, this.confirmPasswordField.nextSibling);
        this.matchText = document.getElementById('password-match-text');
    }

    calculateStrength(password) {
        let score = 0;
        const checks = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /\d/.test(password),
            symbol: /[!@#$%^&*()_,.?":{}|<>]/.test(password)
        };

        Object.values(checks).forEach(check => {
            if (check) score += 20;
        });

        if (password.length > 12) score += 10;
        
        if (password.toLowerCase().includes('password') || 
            password.toLowerCase().includes('123456')) {
            score -= 30;
        }

        return { score: Math.max(0, Math.min(100, score)), checks };
    }

    updateStrengthIndicator() {
        const password = this.passwordField.value;
        
        if (password.length === 0) {
            this.resetStrengthIndicator();
            return;
        }

        const { score, checks } = this.calculateStrength(password);
        
        this.strengthFill.style.width = `${score}%`;
        
        let strengthClass, strengthText;
        if (score < 40) {
            strengthClass = 'weak';
            strengthText = 'Poor';
        } else if (score < 80) {
            strengthClass = 'medium';
            strengthText = 'Medium';
        } else {
            strengthClass = 'strong';
            strengthText = 'Strong';
        }

        this.strengthFill.className = `password-strength-fill ${strengthClass}`;
        this.strengthText.querySelector('.strength-status').textContent = `${strengthText}`;

        this.updateRequirement('req-length', checks.length);
        this.updateRequirement('req-uppercase', checks.uppercase);
        this.updateRequirement('req-number', checks.number);
        this.updateRequirement('req-symbol', checks.symbol);

        const allMet = Object.values(checks).every(check => check);
        this.requirements.style.display = allMet ? 'none' : 'block';
    }

    updateRequirement(id, isMet) {
        const element = document.getElementById(id);
        const icon = element.querySelector('.req-icon');
        
        if (isMet) {
            element.classList.add('met');
            icon.textContent = '✅';
        } else {
            element.classList.remove('met');
            icon.textContent = '❌';
        }
    }

    updatePasswordMatchIndicator() {
        if (!this.confirmPasswordField || !this.matchText) return;

        const password = this.passwordField.value;
        const confirmPassword = this.confirmPasswordField.value;
        const statusElement = this.matchText.querySelector('.match-status');

        if (confirmPassword.length === 0) {
            statusElement.textContent = '';
            this.matchText.className = 'password-match-text';
            return;
        }

        if (password === confirmPassword) {
            statusElement.textContent = '✅ Passwords match';
            this.matchText.className = 'password-match-text match';
        } else {
            statusElement.textContent = '❌ Passwords do not match';
            this.matchText.className = 'password-match-text no-match';
        }
    }

    resetStrengthIndicator() {
        if (this.strengthFill) {
            this.strengthFill.style.width = '0%';
            this.strengthFill.className = 'password-strength-fill';
            this.strengthText.querySelector('.strength-status').textContent = 'Poor';
            
            ['req-length', 'req-uppercase', 'req-number', 'req-symbol'].forEach(id => {
                this.updateRequirement(id, false);
            });
            
            this.requirements.style.display = 'block';
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new PasswordStrengthIndicator('id_password1', 'id_password2');
    
    // Auto-fade messages
    setTimeout(function() {
        var messages = document.querySelectorAll('.messages');
        messages.forEach(function(messageContainer) {
            if (messageContainer) {
                messageContainer.style.transition = "opacity 1s ease-out";
                messageContainer.style.opacity = "0";
                setTimeout(function() {
                    messageContainer.style.display = "none";
                }, 1000);
            }
        });
    }, 3000); // Fade out after 3 seconds
});