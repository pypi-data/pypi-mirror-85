(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9795],{9795:function(){function t(){var e=r(["\n      #head {\n        --toggle-icon-width: 40px;\n        display: flex;\n        cursor: pointer;\n        align-items: center;\n      }\n      #head entity-row-maker {\n        flex-grow: 1;\n        max-width: calc(100% - var(--toggle-icon-width));\n      }\n      #head ha-icon {\n        width: var(--toggle-icon-width);\n        cursor: pointer\n      }\n\n      #items {\n        padding: 0;\n        margin: 0;\n        overflow: hidden;\n        max-height: 0;\n      }\n      #items[open] {\n        overflow: visible;\n        max-height: none;\n      }\n      .state-card-dialog {\n        cursor: pointer;\n      }\n    "]);return t=function(){return e},e}function e(){var t=r(["\n        <entity-row-maker\n          .config=","\n          .hass=","\n          @click=","\n          class=","\n        ></entity-row-maker>\n      "]);return e=function(){return t},t}function n(){var t=r(['\n    <div id="head" ?open=',">\n      <entity-row-maker\n        .config=","\n        .hass=","\n        @click=","\n        head\n      ></entity-row-maker>\n      <ha-icon\n        @click=","\n        icon=",'\n      ></ha-icon>\n    </div>\n\n    <div id="items"\n      ?open=',"\n      style=\n        ","\n    >\n      ","\n    </div>\n    "]);return n=function(){return t},t}function i(){var t=r(["",""]);return i=function(){return t},t}function r(t,e){return e||(e=t.slice(0)),Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}function o(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function s(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}function a(t,e,n){return e&&s(t.prototype,e),n&&s(t,n),t}function u(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&c(t,e)}function c(t,e){return(c=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t})(t,e)}function l(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}();return function(){var n,i=h(t);if(e){var r=h(this).constructor;n=Reflect.construct(i,arguments,r)}else n=i.apply(this,arguments);return f(this,n)}}function f(t,e){return!e||"object"!==p(e)&&"function"!=typeof e?function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t):e}function h(t){return(h=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}function p(t){return(p="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}!function(t){var e={};function n(i){if(e[i])return e[i].exports;var r=e[i]={i:i,l:!1,exports:{}};return t[i].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=t,n.c=e,n.d=function(t,e,i){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==p(t)&&t&&t.__esModule)return t;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var r in t)n.d(i,r,function(e){return t[e]}.bind(null,r));return i},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=0)}([function(r,s,c){"use strict";c.r(s);var f=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),h=f.prototype.html,d=f.prototype.css;var y="custom:",m=["input_number","input_select","input_text","scene","weblink"];function g(t,e){var n=document.createElement("hui-error-card");return n.setConfig({type:"error",error:t,config:e}),n}function v(t,e){if(!e||"object"!=p(e)||!e.type)return g("No ".concat(t," type configured"),e);var n=e.type;if(n=n.startsWith(y)?n.substr(y.length):"hui-".concat(n,"-").concat(t),customElements.get(n))return function(t,e){var n=document.createElement(t);try{n.setConfig(e)}catch(t){return g(t,e)}return n}(n,e);var i=g("Custom element doesn't exist: ".concat(n,"."),e);i.style.display="None";var r=setTimeout((function(){i.style.display=""}),2e3);return customElements.whenDefined(n).then((function(){clearTimeout(r),function(t,e){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null;if((t=new Event(t,{bubbles:!0,cancelable:!1,composed:!0})).detail=e||{},n)n.dispatchEvent(t);else{var i=document.querySelector("home-assistant");(i=(i=(i=(i=(i=(i=(i=(i=(i=(i=(i=i&&i.shadowRoot)&&i.querySelector("home-assistant-main"))&&i.shadowRoot)&&i.querySelector("app-drawer-layout partial-panel-resolver"))&&i.shadowRoot||i)&&i.querySelector("ha-panel-lovelace"))&&i.shadowRoot)&&i.querySelector("hui-root"))&&i.shadowRoot)&&i.querySelector("ha-app-layout #view"))&&i.firstElementChild)&&i.dispatchEvent(t)}}("ll-rebuild",{},i)})),i}var b=function(t){u(n,t);var e=l(n);function n(){return o(this,n),e.apply(this,arguments)}return a(n,[{key:"setConfig",value:function(t){this._config=t,this.el?this.el.setConfig(t):this.el=this.create(t),this._hass&&(this.el.hass=this._hass),this.noHass&&(this,document.querySelector("home-assistant").provideHass(this))}},{key:"createRenderRoot",value:function(){return this}},{key:"render",value:function(){return h(i(),this.el)}},{key:"config",set:function(t){this.setConfig(t)}},{key:"hass",set:function(t){this._hass=t,this.el&&(this.el.hass=t)}}],[{key:"properties",get:function(){return{hass:{},config:{},noHass:{type:Boolean}}}}]),n}(f);if(!customElements.get("card-maker")){var _=function(t){u(n,t);var e=l(n);function n(){return o(this,n),e.apply(this,arguments)}return a(n,[{key:"create",value:function(t){return function(t){return v("card",t)}(t)}},{key:"getCardSize",value:function(){return this.firstElementChild&&this.firstElementChild.getCardSize?this.firstElementChild.getCardSize():1}}]),n}(b);customElements.define("card-maker",_)}if(!customElements.get("element-maker")){var w=function(t){u(n,t);var e=l(n);function n(){return o(this,n),e.apply(this,arguments)}return a(n,[{key:"create",value:function(t){return function(t){return v("element",t)}(t)}}]),n}(b);customElements.define("element-maker",w)}if(!customElements.get("entity-row-maker")){var k=function(t){u(n,t);var e=l(n);function n(){return o(this,n),e.apply(this,arguments)}return a(n,[{key:"create",value:function(t){return function(t){var e=new Set(["call-service","divider","section","weblink"]);if(!t)return g("Invalid configuration given.",t);if("string"==typeof t&&(t={entity:t}),"object"!=p(t)||!t.entity&&!t.type)return g("Invalid configuration given.",t);var n=t.type||"default";if(e.has(n)||n.startsWith(y))return v("row",t);var i=t.entity.split(".",1)[0];return Object.assign(t,{type:{alert:"toggle",automation:"toggle",climate:"climate",cover:"cover",fan:"toggle",group:"group",input_boolean:"toggle",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",remote:"toggle",scene:"scene",script:"script",sensor:"sensor",timer:"timer",switch:"toggle",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime"}[i]||"text"}),v("entity-row",t)}(t)}}]),n}(b);customElements.define("entity-row-maker",k)}customElements.define("hui-ais-fold-entity-row-card",function(i){u(s,i);var r=l(s);function s(){return o(this,s),r.apply(this,arguments)}return a(s,[{key:"setConfig",value:function(t){this._config=Object.assign({},{open:!1,padding:20,group_config:{}},t),this.open=this.open||this._config.open,this.head=this._config.head,this._config.entity&&(this.head=this._config.entity),"string"==typeof this.head&&(this.head={entity:this.head}),this.items=this._config.items,this._config.entities&&(this.items=this._config.entities),this.head.entity&&this.head.entity.startsWith("group.")&&!this.items&&(this.items=document.querySelector("home-assistant").hass.states[this.head.entity].attributes.entity_id)}},{key:"clickRow",value:function(t){t.stopPropagation();var e=t.target.parentElement._config;this.hasMoreInfo(e)||e.tap_action?customElements.get("hui-entities-card").prototype._handleClick.bind(this)(e):t.target.parentElement.hasAttribute("head")&&this.toggle(t)}},{key:"toggle",value:function(t){t&&t.stopPropagation(),this.open=!this.open}},{key:"hasMoreInfo",value:function(t){var e=t.entity||("string"==typeof t?t:null);return!(!e||m.includes(e.split(".",1)[0]))}},{key:"firstUpdated",value:function(){var t=this.shadowRoot.querySelector("#head > entity-row-maker");t.updateComplete.then((function(){var e=t.querySelector("hui-section-row");e&&e.updateComplete.then((function(){e.shadowRoot.querySelector(".divider").style.marginRight="-56px"}))}))}},{key:"render",value:function(){var t=this;this._entities&&this._entities.forEach((function(e){return e.hass=t._hass}));return h(n(),this.open,this.head,this._hass,this.clickRow,this.toggle,this.open?"mdi:chevron-up":"mdi:chevron-down",this.open,this._config.padding?"padding-left: ".concat(this._config.padding,"px;"):"",this.items.map((function(n){return h(e(),("string"==typeof(i=n)&&(i={entity:i}),Object.assign({},t._config.group_config,i)),t._hass,t.clickRow,t.hasMoreInfo(n)?"state-card-dialog":"");var i})))}},{key:"hass",set:function(t){this._hass=t}}],[{key:"properties",get:function(){return{_hass:{},open:Boolean,items:{}}}},{key:"styles",get:function(){return d(t())}}]),s}(f))}])}}]);
//# sourceMappingURL=chunk.2ee9427e177cd446e5c0.js.map