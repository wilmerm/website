
function getValue(selector) {
    try {
        return document.querySelector(selector).value;
    } catch (error) {
        console.warn(error);
        return "";
    }
}

const URL = {
    api_message_form: getValue("#url1")
}
const SITE = {
    title: getValue("#var1"),
    name: getValue("#var1"),
    icon: getValue("#var2"),
    logo: getValue("#var3"),
    phone1: getValue("#var4"),
}


const App = {
    data() {
        return {
            mounted_ok: false,
            html: {
                title: SITE.title,
                head: {
                    show: true,
                },
                body: {
                    show: true,
                    cover: {
                        show: true,
                    },
                    carousel: {
                        show: false,
                    },
                    map: {
                        show: false,
                    },
                    navbar: {
                        show: false,
                    },
                    header: {
                        show: false,
                    },
                    about: {
                        show: false,
                    },
                    main: {
                        show: false,
                    },
                    contact: {
                        show: false,
                        alert: {
                            type: "info",
                            message: ""
                        },
                        form: {
                            name: "",
                            phone: "",
                            email: "",
                            message: "",
                            errors: {
                                name: [],
                                email: [],
                                phone: [],
                                message: []                            
                            }
                        }
                    },
                    footer: {
                        show: false,
                    },
                }
            },
            site: SITE,
        }
    },
    created() {
        
    },
    mounted() {
        this.mounted_ok = true;
        this.html.body.cover.show = true;
        this.html.body.carousel.show = true;
        this.html.body.navbar.show = true;
        this.html.body.map.show = true;
        this.html.body.header.show = true;
        this.html.body.about.show = true;
        this.html.body.main.show = true;
        this.html.body.contact.show = true;
        this.html.body.footer.show = true;
    },
    updated() {

    },
    unmounted() {

    },
    methods: {
        onMessageSubmit(e) {
            _this = this
            e.preventDefault();
            grecaptcha.ready(function() {
                grecaptcha.execute('6LeRs-0aAAAAAEtuUEs-bpdwbzDJm4bAV3kXz8LS', {action: 'submit'}).then(function(token) {
                    let formData = new FormData(document.querySelector("#contact form"));
                    fetch(URL.api_message_form, {
                        method: "POST",
                        mode: "same-origin",
                        //headers: {"Content-Type": "application/json", "cf"},
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        let errors = {name: [], email: [], phone: [], message: []};
                        if (data.error) {
                            _this.html.body.contact.alert.type = "warning";
                            try {
                                errors = JSON.parse(data.errors);
                            } catch (error) {
                                errors = data.errors;
                            }
                        } else {
                            _this.html.body.contact.alert.type = "info";
                        }
                        _this.html.body.contact.form.errors.name = errors.name || [];
                        _this.html.body.contact.form.errors.email = errors.email || [];
                        _this.html.body.contact.form.errors.phone = errors.phone || [];
                        _this.html.body.contact.form.errors.message = errors.message || [];
                        if (data.message) {
                            _this.html.body.contact.alert.message = data.message;
                        }
                    })
                    .catch(error => {
                        _this.html.body.contact.alert.type = "danger";
                        _this.html.body.contact.alert.message = "No pudimos recibir su mensaje. Inténtelo nuevamente.";
                        console.error(error);
                    })
                });
            });
          }
    }
}

const app = Vue.createApp(App);

// Add here components...

app.mount("#app");