Method: POST<br>
Endpoint: https://login.grandid.com/<br>
Response Type: html

---

Response after entering wrong credentials:
Status Code: 200 (for some weird reason)

````html
<!DOCTYPE html>
<html class="no-js" lang="">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <title>AcadeMedia</title>
    <meta name="description" content="" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <link
      rel="stylesheet"
      href="https://cdn.grandid.com/academedia/design/css/main.css?v=1.6"
    />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
  </head>
  <body>
    <h1 class="logo"><a>AcadeMedia</a></h1>

    <article class="container">
      <form class="form" method="POST">
        <input type="hidden" name="fc" value="" />
        <input
          type="hidden"
          name="grandidsession"
          value="bcde60f24fb6e13d40b4ed7a2545de62"
        />
        <input type="hidden" name="idpPlugin" value="true" />
        <div class="form__form-group">
          <div class="form__form-group-header">
            <label class="form__label" for="username">Användarnamn</label>
          </div>
          <input
            class="form__input-text"
            type="text"
            id="username"
            name="username"
            placeholder="fornamn.efternamn"
            autofocus
          />
        </div>
        <div class="form__form-group">
          <div class="form__form-group-header">
            <label class="form__label" for="password">Lösenord</label>
            <a
              target="_blank"
              tabindex="-1"
              href="https://konto.academedia.se"
              class="form__helper-link"
              >Glömt lösenord?</a
            >
          </div>
          <input
            class="form__input-text"
            type="password"
            id="password"
            name="password"
            placeholder="Skriv in ditt lösenord här"
          />
        </div>
        <div class="form__form-group">
          <button class="form__button form__button--primary">Logga in</button>
        </div>
        <p
          class="form__transport-text"
          style="color: #d41121; font-weight: 450;"
        >
          Ange ditt användarnamn och lösenord. Vårdnadshavare och de som fått
          särskild instruktion om detta kan använda Mobilt BankID.
        </p>
        <div class="form__form-group">
          <div class="form__icon-group form__icon-group--left">
            <i class="form__icon"
              ><img
                src="https://cdn.grandid.com/academedia/design/images/bankid.svg"
            /></i>
            <a
              href="?sessionid=bcde60f24fb6e13d40b4ed7a2545de62&bankid=1"
              class="form__button"
              >Logga in med Mobilt BankID</a
            >
          </div>
        </div>
      </form>
    </article>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://cdn.grandid.com/academedia/design/lib/main.js?v=1.2"></script>
  </body>
</html>
```html
````
