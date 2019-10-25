
{{ user.display_name }}（{{ user.email }}）さま

    Code Essay をご利用いただき、ありがとうございます。

    下記URLよりサイトにアクセスの上、メールアドレスの変更を完了してください。
    まだメールアドレスの変更は完了しておりませんので、ご注意ください。

    メールアドレス変更完了用URL
    {{ protocol}}://{{ domain }}{% url 'sign:email_change_complete' token %}

    Code Essay 運営チーム
