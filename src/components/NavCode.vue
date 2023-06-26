<template>
    <div>
    <div class="dropdown">
        <button @click="downloadProject" class="download-button external-links"
            title="Download the generated code as a zip file">
            
            <span>&lt;&gt; Code</span>
        </button>
        <div class="dropdown-content">
            <h1>Local </h1>
            <div class="copy-link">

                <button v-if="!linkGenerated" class="copy-link-input generate" @click="generateLink">Generate Link</button>
                <input v-if="linkGenerated" type="text" class="copy-link-input" v-model="codeUrl" readonly>
                <button type="button" class="copy-link-button" @click="copyURL">
                    <span class="material-icons">content_copy</span>
                </button>
            </div>
           <NavDownload @showDownloadMsg="DownloadMsg" />
        </div>
    </div>
    <div
        class="download-success"
        v-show="showDownloadMsg"
        @click="showDownloadMsg = false"
      ></div>
    <div class="msg-wrapper" v-show="showDownloadMsg">
        <div class="msg">
          <h2>🎉 Your Training Script Has Been Generated! 🎉</h2>
          <p>
            Thanks for using Code-Generator! Feel free to reach out to us on
            <a
              class="external-links msg-gh"
              href="https://github.com/pytorch-ignite/code-generator"
              target="_blank"
              rel="noopener noreferrer"
              >GitHub</a
            >
            with any feedback, bug report, and feature request.
          </p>
        </div>
      </div>
    </div>
</template>

<script>
import NavDownload from '../NavDownload.vue';
import {ref, watch} from "vue";
import { store, msg } from '../../store'

export default {
    name: "NavCode",
    components: { NavDownload },
    setup(){
        const linkGenerated = ref(false);
        const codeUrl = ref(null);
        const showDownloadMsg = ref(false);

        const generateLink = async () => {
            if (store.code && Object.keys(store.code).length) {
                msg.color = 'red'
                if (!store.config.output_dir) {
                    msg.showMsg = true
                    msg.content = `Output directory is required. Please input in Loggers tab.`
                } else if (!store.config.log_every_iters) {
                    msg.showMsg = true
                    msg.content = `Logging interval is required. Please input in Loggers tab.`
                } else {
                    // By default, Netlify function url is
                    // base netlify url + .netlify/functions/function-name
                    // We make a POST request to the function with
                    // the content of store.code in JSON as request body
                    if (store.codeUrl == "") {
                        console.log("test")
                        const res = await fetch('/.netlify/functions/colab', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                code: store.code,
                                template: store.config.template
                            })
                        })
                        // response body is plain text
                        store.codeUrl = await res.json().url;
                        linkGenerated.value = true;
                        codeUrl.value = await res.json().url;
                    }else{
                        linkGenerated.value = true;
                        codeUrl.value = store.codeUrl;
                    }
                }
            } else {
                msg.showMsg = true
                msg.content = 'Choose a template to Open.'
            }
        }
        const DownloadMsg = () => {
            showDownloadMsg.value = True;
        }
        const copyURL = (codeUrl) => {
            try {
                navigator.clipboard.writeText(codeUrl.value);
                alert('Copied');
            } catch ($e) {
                alert('Cannot copy');
            }
        }
        
        watch(store.codeUrl, () => {linkGenerated.value = false});

        return {linkGenerated, generateLink, codeUrl, showDownloadMsg, DownloadMsg, copyURL }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.dropdown{
    align-content: center;
    text-align: center;
}
.download-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: none;
    color: var(--c-text);
    cursor: pointer;
    font-family: var(--font-family-base);
    font-size: 1em;
    padding: 0.5rem 1rem;
    border: 1px solid var(--c-brand-red);
    border-radius: 4px;
}

.download-button span {
    margin-left: 0.25rem;
}

.download-success {
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(101, 110, 133, 0.8);
    z-index: 10;
    width: 100vw;
    height: 100vh;
}

.msg-wrapper {
    position: fixed;
    max-width: 38rem;
    padding: 0 1rem;
    text-align: center;
    margin: 20vh auto 100%;
    inset: 0;
    z-index: 12;
}

.msg {
    padding: 2rem 1rem;
    background-color: var(--c-white-light);
    color: var(--c-text);
    border-radius: 8px;
    box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.33);
}

.msg-gh {
    margin: 0;
    color: var(--c-brand-red);
}

/* Dropdown Button */
.dropbtn {
    background-color: #04AA6D;
    color: white;
    padding: 16px;
    font-size: 16px;
    border: none;
}

/* The container <div> - needed to position the dropdown content */
.dropdown {
    position: relative;
    display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f1f1f1;
    min-width: 300px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 1;
    padding: 20px;
}

/* Links inside the dropdown */
.dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    border:#de4c2c;
    
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {
    background-color: #de4c2c;
    color: #f1f1f1;
}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-content {
    display: block;
}

/* Change the background color of the dropdown button when the dropdown content is shown */
.dropdown:hover .dropbtn {
    background-color: #de4c2c;
}

.copy-link {
    --height: 36px;

    display: flex;
    max-width: 250px;
    margin: 10%;
    margin-top: 20%;
}

.generate {
    background-color: white;
    border-bottom-color: #3e8e41;

}

.copy-link-input {
    flex-grow: 1;
    padding: 0 8px;
    font-size: 14px;
    border: 1px solid #de4c2c;
    border-right: none;
    outline: none;
}

.copy-link-input:hover {
    background: #de4c2c;
    border: 1px solid #cccccc;
    color: #f1f1f1;
}

.copy-link-button {
    flex-shrink: 0;
    width: var(--height);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
    background: #dddddd;
    color: #333333;
    outline: none;
    border: 1px solid #de4c2c;
    cursor: pointer;
}

.copy-link-button:hover {
    background: #cccccc;
}
</style>