(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8558],{47181:function(e,t,n){"use strict";n.d(t,{B:function(){return r}});var r=function(e,t,n,r){r=r||{},n=null==n?{}:n;var i=new Event(t,{bubbles:void 0===r.bubbles||r.bubbles,cancelable:Boolean(r.cancelable),composed:void 0===r.composed||r.composed});return i.detail=n,e.dispatchEvent(i),i}},87744:function(e,t,n){"use strict";function r(e){var t=e.language||"en";return e.translationMetadata.translations[t]&&e.translationMetadata.translations[t].isRTL||!1}function i(e){return o(r(e))}function o(e){return e?"rtl":"ltr"}n.d(t,{HE:function(){return r},Zu:function(){return i},$3:function(){return o}})},68558:function(e,t,n){"use strict";n.r(t),n.d(t,{HuiHumidifierCard:function(){return M}});n(32333);var r=n(15652),i=n(5778),o=n(47181),s=n(91741),a=n(87744),c=(n(22098),n(10983),n(56007)),u=n(64588),l=n(53658),d=n(75502);function f(e){return(f="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function h(){var e=x(["\n      :host {\n        display: block;\n      }\n\n      ha-card {\n        height: 100%;\n        position: relative;\n        overflow: hidden;\n        --name-font-size: 1.2rem;\n        --brightness-font-size: 1.2rem;\n        --rail-border-color: transparent;\n      }\n\n      .more-info {\n        position: absolute;\n        cursor: pointer;\n        top: 0;\n        right: 0;\n        border-radius: 100%;\n        color: var(--secondary-text-color);\n        z-index: 25;\n      }\n\n      .content {\n        height: 100%;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n      }\n\n      #controls {\n        display: flex;\n        justify-content: center;\n        padding: 16px;\n        position: relative;\n      }\n\n      #slider {\n        height: 100%;\n        width: 100%;\n        position: relative;\n        max-width: 250px;\n        min-width: 100px;\n      }\n\n      round-slider {\n        --round-slider-path-color: var(--disabled-text-color);\n        --round-slider-bar-color: var(--mode-color);\n        padding-bottom: 10%;\n      }\n\n      #slider-center {\n        position: absolute;\n        width: calc(100% - 40px);\n        height: calc(100% - 40px);\n        box-sizing: border-box;\n        border-radius: 100%;\n        left: 20px;\n        top: 20px;\n        text-align: center;\n        overflow-wrap: break-word;\n        pointer-events: none;\n      }\n\n      #humidity {\n        position: absolute;\n        transform: translate(-50%, -50%);\n        width: 100%;\n        height: 50%;\n        top: 45%;\n        left: 50%;\n      }\n\n      #set-values {\n        max-width: 80%;\n        transform: translate(0, -50%);\n        font-size: 20px;\n      }\n\n      #set-mode {\n        fill: var(--secondary-text-color);\n        font-size: 16px;\n      }\n\n      #info {\n        display: flex-vertical;\n        justify-content: center;\n        text-align: center;\n        padding: 16px;\n        margin-top: -60px;\n        font-size: var(--name-font-size);\n      }\n\n      #modes > * {\n        color: var(--disabled-text-color);\n        cursor: pointer;\n        display: inline-block;\n      }\n\n      #modes .selected-icon {\n        color: var(--mode-color);\n      }\n\n      text {\n        fill: var(--primary-text-color);\n      }\n    "]);return h=function(){return e},e}function p(){var e=x(['\n      <ha-card>\n        <ha-icon-button\n          icon="hass:dots-vertical"\n          class="more-info"\n          @click=','\n          tabindex="0"\n        ></ha-icon-button>\n\n        <div class="content">\n          <div id="controls">\n            <div id="slider">\n              ','\n              <div id="slider-center">\n                <div id="humidity">\n                  ','\n                </div>\n              </div>\n            </div>\n          </div>\n          <div id="info">\n            ',"\n          </div>\n        </div>\n      </ha-card>\n    "]);return p=function(){return e},e}function m(){var e=x(["\n                    -\n                    ","\n                  "]);return m=function(){return e},e}function y(){var e=x(["\n                    ",'\n                    <tspan dx="-3" dy="-6.5" style="font-size: 4px;">\n                      %\n                    </tspan>\n                    ']);return y=function(){return e},e}function v(){var e=x(['\n      <svg viewBox="0 0 40 20">\n        <text\n          x="50%"\n          dx="1"\n          y="60%"\n          text-anchor="middle"\n          style="font-size: 13px;"\n          class="set-value"\n        >\n          ','\n        </text>\n      </svg>\n      <svg id="set-values">\n        <g>\n          <text\n            dy="22"\n            text-anchor="middle"\n            id="set-mode"\n          >\n            ',"\n            ","\n          </text>\n        </g>\n      </svg>\n    "]);return v=function(){return e},e}function b(){var e=x(["\n          <round-slider\n            .value=","\n            .min=","\n            .max=","\n            .rtl=",'\n            step="1"\n            @value-changing=',"\n            @value-changed=","\n          ></round-slider>\n        "]);return b=function(){return e},e}function g(){var e=x([' <round-slider disabled="true"></round-slider> ']);return g=function(){return e},e}function w(){var e=x(["\n        <hui-warning>\n          ","\n        </hui-warning>\n      "]);return w=function(){return e},e}function k(){var e=x([""]);return k=function(){return e},e}function x(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function E(e,t,n,r,i,o,s){try{var a=e[o](s),c=a.value}catch(u){return void n(u)}a.done?t(c):Promise.resolve(c).then(r,i)}function _(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function P(e,t){return(P=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function S(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=B(e);if(t){var i=B(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return z(this,n)}}function z(e,t){return!t||"object"!==f(t)&&"function"!=typeof t?C(e):t}function C(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function O(){O=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!D(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var u=c.extras;if(u){for(var l=0;l<u.length;l++)this.addElementPlacement(u[l],t);n.push.apply(n,u)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return F(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?F(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=H(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:T(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=T(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function j(e){var t,n=H(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function A(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function D(e){return e.decorators&&e.decorators.length}function R(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function T(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function H(e){var t=function(e,t){if("object"!==f(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==f(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===f(t)?t:String(t)}function F(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function I(e,t,n){return(I="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=B(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}})(e,t,n||e)}function B(e){return(B=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var M=function(e,t,n,r){var i=O();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var s=t((function(e){i.initializeInstanceElements(e,a.elements)}),n),a=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(R(o.descriptor)||R(i.descriptor)){if(D(o)||D(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(D(o)){if(D(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}A(o,i)}else t.push(o)}return t}(s.d.map(j)),e);return i.initializeClassElements(s.F,a.elements),i.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("hui-humidifier-card")],(function(e,t){var f,x,z=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&P(e,t)}(r,t);var n=S(r);function r(){var t;_(this,r);for(var i=arguments.length,o=new Array(i),s=0;s<i;s++)o[s]=arguments[s];return t=n.call.apply(n,[this].concat(o)),e(C(t)),t}return r}(t);return{F:z,d:[{kind:"method",static:!0,key:"getConfigElement",value:(f=regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([n.e(5009),n.e(8161),n.e(4358),n.e(1041),n.e(8374),n.e(7910),n.e(8426),n.e(3918),n.e(3437),n.e(4268),n.e(3648),n.e(8946),n.e(8746),n.e(4535),n.e(6938)]).then(n.bind(n,57210));case 2:return e.abrupt("return",document.createElement("hui-humidifier-card-editor"));case 3:case"end":return e.stop()}}),e)})),x=function(){var e=this,t=arguments;return new Promise((function(n,r){var i=f.apply(e,t);function o(e){E(i,n,r,o,s,"next",e)}function s(e){E(i,n,r,o,s,"throw",e)}o(void 0)}))},function(){return x.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,n){return{type:"humidifier",entity:(0,u.j)(e,1,t,n,["humidifier"])[0]||""}}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_setHum",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 6}},{kind:"method",key:"setConfig",value:function(e){if(!e.entity||"humidifier"!==e.entity.split(".")[0])throw new Error("Specify an entity from within the humidifier domain.");this._config=e}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return(0,r.dy)(k());var e=this.hass.states[this._config.entity];if(!e)return(0,r.dy)(w(),(0,d.i)(this.hass,this._config.entity));var t=this._config.name||(0,s.C)(this.hass.states[this._config.entity]),n=null!==e.attributes.humidity&&Number.isFinite(Number(e.attributes.humidity))?e.attributes.humidity:e.attributes.min_humidity,i=(0,a.Zu)(this.hass),o=c.V_.includes(e.state)?(0,r.dy)(g()):(0,r.dy)(b(),n,e.attributes.min_humidity,e.attributes.max_humidity,"rtl"===i,this._dragEvent,this._setHumidity),u=(0,r.YP)(v(),c.V_.includes(e.state)||void 0===this._setHum||null===this._setHum?"":(0,r.YP)(y(),this._setHum.toFixed()),this.hass.localize("state.default.".concat(e.state)),e.attributes.mode&&!c.V_.includes(e.state)?(0,r.dy)(m(),this.hass.localize("state_attributes.humidifier.mode.".concat(e.attributes.mode))||e.attributes.mode):"");return(0,r.dy)(p(),this._handleMoreInfo,o,u,t)}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,l.G)(this,e)}},{kind:"method",key:"updated",value:function(e){if(I(B(z.prototype),"updated",this).call(this,e),this._config&&this.hass&&(e.has("hass")||e.has("_config"))){var t=e.get("hass"),n=e.get("_config");t&&n&&t.themes===this.hass.themes&&n.theme===this._config.theme||(0,i.R)(this,this.hass.themes,this._config.theme);var r=this.hass.states[this._config.entity];r&&(t&&t.states[this._config.entity]===r||(this._setHum=this._getSetHum(r),this._rescale_svg()))}}},{kind:"method",key:"_rescale_svg",value:function(){var e=this;this.shadowRoot&&this.shadowRoot.querySelector("ha-card")&&this.shadowRoot.querySelector("ha-card").updateComplete.then((function(){var t=e.shadowRoot.querySelector("#set-values"),n=t.querySelector("g").getBBox();t.setAttribute("viewBox","".concat(n.x," ").concat(n.y," ").concat(n.width," ").concat(n.height)),t.setAttribute("width","".concat(n.width)),t.setAttribute("height","".concat(n.height))}))}},{kind:"method",key:"_getSetHum",value:function(e){if(!c.V_.includes(e.state))return e.attributes.humidity}},{kind:"method",key:"_dragEvent",value:function(e){this._setHum=e.detail.value}},{kind:"method",key:"_setHumidity",value:function(e){this.hass.callService("humidifier","set_humidity",{entity_id:this._config.entity,humidity:e.detail.value})}},{kind:"method",key:"_handleMoreInfo",value:function(){(0,o.B)(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,r.iv)(h())}}]}}),r.oi)}}]);
//# sourceMappingURL=chunk.fe332dc9c62ceb74746b.js.map