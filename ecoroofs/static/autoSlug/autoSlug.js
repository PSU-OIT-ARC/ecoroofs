/*
* Javascript module to support custom Django AutoSlugField
*
* Requires slug input name to be "slug".
* Sets slug field to readonly.
* Derives value for slug field from source input.
* Source input is identified by 'data-source' attribute on slug field.
* Asyncrounously fetches new slug from sluggify endpoint on source field's blur
* event or on form submit (if source input value has changed).
* Requires user to validate changes to slug via confirmation buttons.
* Endpoint identified by 'data-endpoint' attribute on slug field.
* Endpoint must take 1 parameter ('name') and return an object with "slug" key/value
* Uses some es6 features which may not be supported in older browsers.
*/


var AutoSlug = (function () {
    "use strict";

    let check_slug,
        get_new_slug,
        choose_slug,
        get,
        init;

    init = function () {
        let slug_field,
            source_selector,
            source_field,
            endpoint,
            original_source_value;

        check_slug = true;

        slug_field = document.querySelector("input[name='slug']");
        slug_field.readOnly = true;
        source_selector = slug_field.getAttribute("data-source");
        source_field = document.querySelector(`input[name='${source_selector}']`);
        original_source_value = source_field.value;
        endpoint = slug_field.getAttribute("data-endpoint");

        source_field.addEventListener("blur", function () {
            check_slug = true;
            get_new_slug(
                source_field.value, original_source_value, slug_field, endpoint
            );
        });

        source_field.form.addEventListener("submit", function (e) {
            if (check_slug) {
                e.preventDefault();
                slug_field.scrollIntoView();
            }
            get_new_slug(
                source_field.value, original_source_value, slug_field, endpoint
            );
        });
    }

    get_new_slug = function (page_name, original_source_value, slug_field, endpoint) {
        let request;

        request = `${endpoint}?name=${page_name}`;
        // no slug yet (eg: new record)
        if (!slug_field.value) {
            get(request)
               .then(JSON.parse)
               .then((response) => {
                   slug_field.setAttribute("value", response.slug);
                })
               .catch(function(error) { throw new Error(error); });
        }
        else {
            // source field has changed
            if (page_name != original_source_value) {
                get(request)
                   .then(JSON.parse)
                   .then((response) => {
                       choose_slug(slug_field.value, response.slug, slug_field);
                   })
                   .catch(function(error) { throw new Error(error); });
            }
        }
    };

    choose_slug = function (old_slug, new_slug, slug_field) {
        /* generate slug confrimation markup and behavior */

        let deny,
            confirm,
            warning,
            warning_ul;

        slug_field.classList.add("warn");
        slug_field.blur();

        warning = `<li>
                     <span>Use new slug: </span>
                     <span class="slug">/${new_slug}</span>?
                   </li>
                   </li>
                     <a class="button" id="slug_yes">Yes</a>
                     <a class="button" id="slug_no">No</a>
                   </li>`;

        if (document.querySelector("ul.slug-update") === null) {
            warning_ul = document.createElement("ul");
            warning_ul.classList.add("slug-update", "warn");
            slug_field.insertAdjacentElement("afterend", warning_ul);
            warning_ul.innerHTML = warning;

        }
        else {
            warning_ul = document.querySelector("ul.slug-update");
            warning_ul.innerHTML = warning;
        }

        confirm = document.querySelector("#slug_yes");
        deny = document.querySelector("#slug_no");

        confirm.addEventListener("click", function() {
            warning_ul.parentElement.removeChild(warning_ul);
            slug_field.setAttribute("value", new_slug);
            check_slug = false;
        });

        deny.addEventListener("click", function() {
            warning_ul.parentElement.removeChild(warning_ul);
            check_slug = false;
        });
    };

    get = function (url) {
            return new Promise(function(resolve, reject) {
                let request = new XMLHttpRequest();
                request.open("GET", url);
                request.onload = function() {
                    if (request.status === 200) {
                        resolve(request.response);
                    } else {
                        reject(new Error(request.statusText));
                    }
                };
                request.onerror = function() {
                    reject(new Error("Network error"));
                };
                request.send();
            });
    }

    return {
        init: init
    };

})();


document.addEventListener("DOMContentLoaded", function () {
    AutoSlug.init();
});
