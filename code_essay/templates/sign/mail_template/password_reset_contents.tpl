
{{ user.display_name }}（{{ user.email }}）さま

    Code Essay をご利用いただき、ありがとうございます。

    下記URLよりサイトにアクセスの上、パスワードの再設定を行ってください。

    パスワード再設定用URL
    {{ protocol}}://{{ domain }}{% url 'sign:password_reset_confirm' uid token %}

    Code Essay 運営チーム
