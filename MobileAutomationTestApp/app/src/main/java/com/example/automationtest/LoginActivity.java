package com.example.automationtest;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class LoginActivity extends AppCompatActivity {
    
    private EditText etUsername;
    private EditText etPassword;
    private Button btnLogin;
    private ProgressBar progressBar;
    private TextView tvRegister;
    private TextView tvForgotPassword;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        
        etUsername = findViewById(R.id.et_username);
        etPassword = findViewById(R.id.et_password);
        btnLogin = findViewById(R.id.btn_login);
        progressBar = findViewById(R.id.progress_bar);
        tvRegister = findViewById(R.id.tv_register);
        tvForgotPassword = findViewById(R.id.tv_forgot_password);
        
        btnLogin.setOnClickListener(v -> attemptLogin());
        
        tvRegister.setOnClickListener(v -> {
            Toast.makeText(this, "跳转到注册页面", Toast.LENGTH_SHORT).show();
        });
        
        tvForgotPassword.setOnClickListener(v -> {
            Toast.makeText(this, "跳转到找回密码页面", Toast.LENGTH_SHORT).show();
        });
    }
    
    private void attemptLogin() {
        String username = etUsername.getText().toString().trim();
        String password = etPassword.getText().toString().trim();
        
        // 验证输入
        if (username.isEmpty()) {
            etUsername.setError("用户名不能为空");
            etUsername.requestFocus();
            return;
        }
        
        if (password.isEmpty()) {
            etPassword.setError("密码不能为空");
            etPassword.requestFocus();
            return;
        }
        
        if (password.length() < 6) {
            etPassword.setError("密码至少6位");
            etPassword.requestFocus();
            return;
        }
        
        // 显示加载
        progressBar.setVisibility(View.VISIBLE);
        btnLogin.setEnabled(false);
        
        // 模拟网络请求
        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            progressBar.setVisibility(View.GONE);
            btnLogin.setEnabled(true);
            
            if (username.equals("admin") && password.equals("123456")) {
                Toast.makeText(this, "登录成功！", Toast.LENGTH_SHORT).show();
                finish();
            } else {
                Toast.makeText(this, "用户名或密码错误", Toast.LENGTH_SHORT).show();
            }
        }, 2000);
    }
}