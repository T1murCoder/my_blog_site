# my_blog_site
Это мой проект на Flask


<h2>О проекте</h2>
<p>
Это мой учебный проект для <b>Яндекс.Лицея</b><br>
Он представляет из себя личный блог, посты для которого берутся из телеграм-канала<br>
<img src="https://user-images.githubusercontent.com/110349339/233779782-e301217f-bc38-425f-8acb-fb4346345cde.png" style="width: 50%; height: 50%"><br>
</p>
<div>
  <h2>Features</h2>
<h3>Возможности пользователя</h3>
<p>
<ul>
  <li>Зарегистрироваться для того, чтобы оценивать и комментировать записи</li>
  <li>Прикладывать до 3-х изображений к комментарию</li>
  <li>Просматривать комментарии</li>
  <li>Редактировать или удалять свои комментарии</li>
  <li>Поставить свою аватарку в профиле</li>
  <li>Сменить пароль</li>
  <li>Сбросить пароль (Если пользователь забыл пароль, то на указанную почту придёт письмо<br> с инструкцией для восстановления)</li>
  <li>Заполнить информацию "О себе"</li>
  <li>Отправлять обратную связь</li>
<ul>
</p>
</div>
<div>
<h3>Возможности администратора</h3>
<p>
<ul>
  <li>Управление постами (Просмотр, создание, удаление)</li>
  <li>Управление пользователями (Просмотр, редактирование прав, удаление)</li>
  <li>Управление токенами API (Просмотр, создание, удаление)</li>
  <li>Удалять комментарии пользователей</li>
  <li>Отвечать на обратную связь (ответ летит на почту пользователя)</li>
<ul>
</p>
</div>
<div>
<h3>API</h3>
<p>
<ul>
  <li>Доступны ресуры: users, posts</li>
  <li>Для использование нужно иметь ключ или админку</li>
  <li>Есть скрипт, облегчающий работу с API</li>
  <li>Возможно использование в других сервисах (Например, общий аккаунт)</li>
  <li>Есть автоматическая публикация постов на сайт, если запущен тг-бот</li>
<ul>
</p>
</div>
<div>
<div>
<h2>Установка</h2>
<p>
<h3>Автоматическая установка на Windows</h3>
  <ol>
    <li>Установите <a href="https://www.python.org/downloads/windows/">Python 3.9.13</a> или выше, и выберите галочку "Add Python to PATH".</li>
    <li>Установите <a href="https://git-scm.com/download/win">git</a>.</li>
    <li>Склонируйте репозиторий <code>git clone https://github.com/T1murCoder/my_blog_site.git</code>.</li>
    <li>Установите необходимые зависимости <code>py -m pip install -r requirements.txt</code>.</li>
    <li>Создайте файл <code>.env</code> на основе <a href="https://github.com/T1murCoder/my_blog_site/files/11304722/cfg.txt">cfg.txt</a> и положите в директорию с <code>app.py</code>.</li>
    <li>Запустите файл <code>app.py</code>.</li>
  </ol>
</p>
</div>

