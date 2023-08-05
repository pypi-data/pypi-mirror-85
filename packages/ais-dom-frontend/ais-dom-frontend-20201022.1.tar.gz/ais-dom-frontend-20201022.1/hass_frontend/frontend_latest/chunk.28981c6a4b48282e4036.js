(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6329],{49706:(e,t,i)=>{"use strict";i.d(t,{Rb:()=>a,Zy:()=>r,h2:()=>n,PS:()=>o,l:()=>s,ht:()=>l,f0:()=>c,tj:()=>d,uo:()=>p,lC:()=>m,Kk:()=>h,ot:()=>u,gD:()=>f,a1:()=>b,AZ:()=>y});const a="hass:bookmark",r={alert:"hass:alert",alexa:"hass:amazon-alexa",air_quality:"hass:air-filter",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:cog",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:toggle-switch-outline",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:form-textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer-outline",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",zone:"hass:map-marker-radius"},n={current:"hass:current-ac",energy:"hass:flash",humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",power_factor:"hass:angle-acute",signal_strength:"hass:wifi",timestamp:"hass:clock",voltage:"hass:sine-wave"},o=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","scene","script","timer","vacuum","water_heater"],s=["alarm_control_panel","automation","camera","climate","configurator","counter","cover","fan","group","humidifier","input_datetime","light","lock","media_player","person","script","sun","timer","vacuum","water_heater","weather"],l=["input_number","input_select","input_text","scene"],c=["camera","configurator","scene"],d=["closed","locked","off"],p="on",m="off",h=new Set(["fan","input_boolean","light","switch","group","automation","humidifier"]),u="°C",f="°F",b="group.default_view",y=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"]},5435:(e,t,i)=>{"use strict";i.d(t,{Z:()=>n});const a=[60,60,24,7],r=["second","minute","hour","day"];function n(e,t,i={}){let n=((i.compareTime||new Date).getTime()-e.getTime())/1e3;const o=n>=0?"past":"future";n=Math.abs(n);let s=Math.round(n);if(0===s)return t("ui.components.relative_time.just_now");let l="week";for(let c=0;c<a.length;c++){if(s<a[c]){l=r[c];break}n/=a[c],s=Math.round(n)}return t(!1===i.includeTense?"ui.components.relative_time.duration."+l:`ui.components.relative_time.${o}_duration.${l}`,"count",s)}},91168:(e,t,i)=>{"use strict";i.d(t,{Z:()=>r});const a=e=>e<10?"0"+e:e;function r(e){const t=Math.floor(e/3600),i=Math.floor(e%3600/60),r=Math.floor(e%3600%60);return t>0?`${t}:${a(i)}:${a(r)}`:i>0?`${i}:${a(r)}`:r>0?""+r:null}},22311:(e,t,i)=>{"use strict";i.d(t,{N:()=>r});var a=i(58831);const r=e=>(0,a.M)(e.entity_id)},83599:(e,t,i)=>{"use strict";i.d(t,{m:()=>a});const a=e=>{if(!e.attributes.remaining)return;let t=function(e){const t=e.split(":").map(Number);return 3600*t[0]+60*t[1]+t[2]}(e.attributes.remaining);if("active"===e.state){const i=(new Date).getTime(),a=new Date(e.last_changed).getTime();t=Math.max(t-(i-a)/1e3,0)}return t}},76111:(e,t,i)=>{"use strict";var a=i(50856),r=(i(54444),i(1265)),n=i(28426),o=i(91741),s=i(87744);i(32075),i(3143);class l extends((0,r.Z)(n.H3)){static get template(){return a.d`
      ${this.styleTemplate} ${this.stateBadgeTemplate} ${this.infoTemplate}
    `}static get styleTemplate(){return a.d`
      <style>
        :host {
          @apply --paper-font-body1;
          min-width: 120px;
          white-space: nowrap;
        }

        state-badge {
          float: left;
        }

        :host([rtl]) state-badge {
          float: right;
        }

        .info {
          margin-left: 56px;
        }

        :host([rtl]) .info {
          margin-right: 56px;
          margin-left: 0;
          text-align: right;
        }

        .name {
          @apply --paper-font-common-nowrap;
          color: var(--primary-text-color);
          line-height: 40px;
        }

        .name[in-dialog],
        :host([secondary-line]) .name {
          line-height: 20px;
        }

        .time-ago,
        .extra-info,
        .extra-info > * {
          @apply --paper-font-common-nowrap;
          color: var(--secondary-text-color);
        }
      </style>
    `}static get stateBadgeTemplate(){return a.d` <state-badge state-obj="[[stateObj]]"></state-badge> `}static get infoTemplate(){return a.d`
      <div class="info">
        <div class="name" in-dialog$="[[inDialog]]">
          [[computeStateName(stateObj)]]
        </div>
        <template is="dom-if" if="[[inDialog]]">
          <div class="time-ago">
            <ha-relative-time
              id="last_changed"
              hass="[[hass]]"
              datetime="[[stateObj.last_changed]]"
            ></ha-relative-time>
            <paper-tooltip animation-delay="0" for="last_changed">
              [[localize('ui.dialogs.more_info_control.last_updated')]]:
              <ha-relative-time
                hass="[[hass]]"
                datetime="[[stateObj.last_updated]]"
              ></ha-relative-time>
            </paper-tooltip>
          </div>
        </template>
        <template is="dom-if" if="[[!inDialog]]">
          <div class="extra-info"><slot> </slot></div>
        </template>
      </div>
    `}static get properties(){return{hass:Object,stateObj:Object,inDialog:{type:Boolean,value:()=>!1},rtl:{type:Boolean,reflectToAttribute:!0,computed:"computeRTL(hass)"}}}computeStateName(e){return(0,o.C)(e)}computeRTL(e){return(0,s.HE)(e)}}customElements.define("state-info",l)},81303:(e,t,i)=>{"use strict";i(8878);const a=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends a{ready(){super.ready(),setTimeout((()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")}),100)}})},32075:(e,t,i)=>{"use strict";var a=i(87156),r=i(28426),n=i(5435),o=i(1265);class s extends((0,o.Z)(r.H3)){static get properties(){return{hass:Object,datetime:{type:String,observer:"datetimeChanged"},datetimeObj:{type:Object,observer:"datetimeObjChanged"},parsedDateTime:Object}}constructor(){super(),this.updateRelative=this.updateRelative.bind(this)}connectedCallback(){super.connectedCallback(),this.updateInterval=setInterval(this.updateRelative,6e4)}disconnectedCallback(){super.disconnectedCallback(),clearInterval(this.updateInterval)}datetimeChanged(e){this.parsedDateTime=e?new Date(e):null,this.updateRelative()}datetimeObjChanged(e){this.parsedDateTime=e,this.updateRelative()}updateRelative(){const e=(0,a.vz)(this);this.parsedDateTime?e.innerHTML=(0,n.Z)(this.parsedDateTime,this.localize):e.innerHTML=this.localize("ui.components.relative_time.never")}}customElements.define("ha-relative-time",s)},43709:(e,t,i)=>{"use strict";i(47356);var a=i(65661),r=i(15652),n=i(62359);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(a){t.forEach((function(t){var r=t.placement;if(t.kind===a&&("static"===r||"prototype"===r)){var n="static"===r?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var a=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],a=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,r);i.push(t.element),i.push.apply(i,t.extras),a.push.apply(a,t.finishers)}),this),!t)return{elements:i,finishers:a};var n=this.decorateConstructor(i,t);return a.push.apply(a,n.finishers),n.finishers=a,n},addElementPlacement:function(e,t,i){var a=t[e.placement];if(!i&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var i=[],a=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&a.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:a,extras:i}},decorateConstructor:function(e,t){for(var i=[],a=t.length-1;a>=0;a--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[a])(r)||r);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:a,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var a=(0,t[i])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function s(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var a=i.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,a=new Array(t);i<t;i++)a[i]=e[i];return a}function u(e,t,i){return(u="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var a=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(a){var r=Object.getOwnPropertyDescriptor(a,t);return r.get?r.get.call(i):r.value}})(e,t,i||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const b=customElements.get("mwc-switch");!function(e,t,i,a){var r=o();if(a)for(var n=0;n<a.length;n++)r=a[n](r);var p=t((function(e){r.initializeInstanceElements(e,m.elements)}),i),m=r.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},a=0;a<e.length;a++){var r,n=e[a];if("method"===n.kind&&(r=t.find(i)))if(d(n.descriptor)||d(r.descriptor)){if(c(n)||c(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(c(n)){if(c(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}l(n,r)}else t.push(n)}return t}(p.d.map(s)),e);r.initializeClassElements(p.F,m.elements),r.runClassFinishers(p.F,m.finishers)}([(0,r.Mo)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){u(f(i.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--switch-checked-color)"),this.addEventListener("change",(()=>{this.haptic&&(0,n.j)("light")}))}},{kind:"get",static:!0,key:"styles",value:function(){return[a.o,r.iv`
        .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
          background-color: var(--switch-checked-button-color);
          border-color: var(--switch-checked-button-color);
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__track {
          background-color: var(--switch-checked-track-color);
          border-color: var(--switch-checked-track-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--switch-unchecked-button-color);
          border-color: var(--switch-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--switch-unchecked-track-color);
          border-color: var(--switch-unchecked-track-color);
        }
      `]}}]}}),b)},43408:(e,t,i)=>{"use strict";i.d(t,{H:()=>a});const a=e=>e.callWS({type:"webhook/list"})},26765:(e,t,i)=>{"use strict";i.d(t,{Ys:()=>o,g7:()=>s,D9:()=>l});var a=i(47181);const r=()=>Promise.all([i.e(8200),i.e(879),i.e(3437),i.e(1458),i.e(3648),i.e(1868),i.e(6509),i.e(7230)]).then(i.bind(i,1281)),n=(e,t,i)=>new Promise((n=>{const o=t.cancel,s=t.confirm;(0,a.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:r,dialogParams:{...t,...i,cancel:()=>{n(!!(null==i?void 0:i.prompt)&&null),o&&o()},confirm:e=>{n(!(null==i?void 0:i.prompt)||e),s&&s(e)}}})})),o=(e,t)=>n(e,t),s=(e,t)=>n(e,t,{confirmation:!0}),l=(e,t)=>n(e,t,{prompt:!0})},1265:(e,t,i)=>{"use strict";i.d(t,{Z:()=>a});const a=(0,i(76389).o)((e=>class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},6942:(e,t,i)=>{"use strict";i.r(t);i(53268),i(12730);var a=i(50856),r=i(28426);i(60010),i(38353),i(63081),i(81303),i(43709),i(8878),i(53973),i(51095),i(54909),i(16509);class n extends r.H3{static get template(){return a.d`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }

        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .card-actions {
          display: flex;
        }
        ha-card > div#card-icon {
          margin: -4px 0;
          position: absolute;
          top: 1em;
          right: 1em;
          border-radius: 25px;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        .config-invalid .text {
          color: var(--google-red-500);
          font-weight: 500;
        }

        @keyframes pulse {
          0% {
            background-color: var(--card-background-color);
          }
          100% {
            background-color: var(--primary-color);
          }
        }
        @keyframes pulseRed {
          0% {
            background-color: var(--card-background-color);
          }
          100% {
            background-color: var(--material-error-color);
          }
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienie zapisu logów systemu</span>
            <span slot="introduction"
              >Tu możesz skonfigurować zapis logów do pliku na wymiennym
              dysku</span
            >
            <ha-card header="Zapis logów systemu do pliku">
              <div id="card-icon" style$="[[logIconAnimationStyle]]">
                <ha-icon-button icon="mdi:record-rec"></ha-icon-button>
              </div>
              <div class="card-content">
                Żeby włączyć logowanie w systemie Asystent domowy, wystarczy
                wybrać lokalizację na dysku wymiennym, w której będzie
                zapisywany plik z rejestrem działań w systemie. <br />
                Dodatkowo można też określić poziom szczegółowości logowania i
                liczbę dni przechowywanych w jednym pliku loga. <br /><br />
                Wybór dysku do zapisu logów systemu: <br />
                <ha-icon-button icon="mdi:usb-flash-drive"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Wybrany dysk"
                  dynamic-align=""
                  label="Dyski wymienne"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[logDrive]]"
                    on-selected-changed="logDriveChanged"
                    attr-for-selected="item-name"
                  >
                    <template
                      is="dom-repeat"
                      items="[[usbDrives.attributes.options]]"
                    >
                      <paper-item item-name$="[[item]]">[[item]]</paper-item>
                    </template>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
              </div>
              <div class="card-content">
                Wybór poziomu logowania: <br />
                <ha-icon-button icon="mdi:bug-check"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Poziom logowania"
                  dynamic-align=""
                  label="Poziomy logowania"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[logLevel]]"
                    on-selected-changed="logLevelChanged"
                    attr-for-selected="item-name"
                  >
                    <paper-item item-name="critical">critical</paper-item>
                    <paper-item item-name="fatal">fatal</paper-item>
                    <paper-item item-name="error">error</paper-item>
                    <paper-item item-name="warning">warning</paper-item>
                    <paper-item item-name="warn">warn</paper-item>
                    <paper-item item-name="info">info</paper-item>
                    <paper-item item-name="debug">debug</paper-item>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
                <br /><br />
                W tym miejscu możesz określić liczbę dni przechowywanych w
                jednym pliku loga. Rotacja plików dziennika wykonywna jest o
                północy.
                <paper-input
                  type="number"
                  value="[[logRotating]]"
                  on-change="logRotatingDaysChanged"
                  maxlength="4"
                  max="9999"
                  min="1"
                  label-float="Liczba dni przechowywanych w jednym pliku loga"
                  label="Liczba dni przechowywanych w jednym pliku loga"
                >
                  <ha-icon icon="mdi:calendar" slot="suffix"></ha-icon>
                </paper-input>
                <div class="config-invalid">
                  <span class="text">
                    [[logError]]
                  </span>
                </div>
              </div>
              <div class="card-content">
                [[logModeInfo]]
              </div>
              <div class="card-content">
                * Zmiana poziomu logowania wykonywana jest online - po tej
                zmianie nie trzeba ponownie uruchomieć systemu. Zastosowanie
                zmiany dysku do zapisu systemu lub zmiany liczby dni
                przechowywanych w jednym pliku loga wymaga restartu systemu.
              </div>
            </ha-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienia zapisu zdarzeń systemu</span>
            <span slot="introduction">
              Tu możesz skonfigurować zapis zdarzeń do bazy danych na dysku
              wymiennym lub do zdalnego serwera bazodanowego
            </span>
            <ha-card header="Zapis zdarzeń do bazy danych">
              <div id="card-icon" style$="[[dbIconAnimationStyle]]">
                <ha-icon-button icon="mdi:database"></ha-icon-button>
              </div>
              <div class="card-content">
                Wybierz silnik bazodanowy, który chcesz użyć do rejestracji
                zdarzeń.<br /><br />Najprostszy wybór to baza SQLite, która nie
                wymaga konfiguracji i może rejestrować dane w pamięci - taka
                baza jest automatycznie używana, gdy rejestracja zdarzeń
                włączana jest przez integrację (np. Historia lub Dziennik).
                <br /><br />Gdy system generuje więcej zdarzeń lub gdy chcesz
                mieć dostęp do historii, to zalecamy zapisywać zdarzenia na
                zewnętrznym dysku lub w zdalnej bazie danych. <br /><br />
                Wybór silnika bazy danych:
                <br />
                <ha-icon-button icon="mdi:database"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Silnik bazy danych"
                  dynamic-align=""
                  label="Silnik bazy danych"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[dbEngine]]"
                    on-selected-changed="dbEngineChanged"
                    attr-for-selected="item-name"
                  >
                    <paper-item item-name="-">-</paper-item>
                    <paper-item item-name="SQLite (memory)"
                      >SQLite (memory)</paper-item
                    >
                    <paper-item item-name="SQLite (file)"
                      >SQLite (file)</paper-item
                    >
                    <paper-item item-name="MariaDB">MariaDB</paper-item>
                    <paper-item item-name="MySQL">MySQL</paper-item>
                    <paper-item item-name="PostgreSQL">PostgreSQL</paper-item>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
              </div>
              <div class="card-content" style$="[[dbFileDisplayStyle]]">
                Wybór dysku do zapisu bazy danych: <br />
                <ha-icon-button icon="mdi:usb-flash-drive"></ha-icon-button>
                <ha-paper-dropdown-menu
                  label-float="Wybrany dysk"
                  dynamic-align=""
                  label="Dyski wymienne"
                >
                  <paper-listbox
                    slot="dropdown-content"
                    selected="[[dbDrive]]"
                    on-selected-changed="dbDriveChanged"
                    attr-for-selected="item-name"
                  >
                    <template
                      is="dom-repeat"
                      items="[[usbDrives.attributes.options]]"
                    >
                      <paper-item item-name$="[[item]]">[[item]]</paper-item>
                    </template>
                  </paper-listbox>
                </ha-paper-dropdown-menu>
                <br /><br />
              </div>
              <div class="card-content" style$="[[dbConectionDisplayStyle]]">
                Parametry połączenia z bazą danych: <br />
                <paper-input
                  placeholder="Użytkownik"
                  type="text"
                  id="db_user"
                  value="[[dbUser]]"
                  on-change="_computeDbUrl"
                >
                  <ha-icon icon="mdi:account" slot="suffix"></ha-icon>
                </paper-input>
                <paper-input
                  placeholder="Hasło"
                  no-label-float=""
                  type="password"
                  id="db_password"
                  value="[[dbPassword]]"
                  on-change="_computeDbUrl"
                  ><ha-icon icon="mdi:lastpass" slot="suffix"></ha-icon
                ></paper-input>
                <paper-input
                  placeholder="IP Serwera DB"
                  no-label-float=""
                  type="text"
                  id="db_server_ip"
                  value="[[dbServerIp]]"
                  on-change="_computeDbUrl"
                  ><ha-icon icon="mdi:ip-network" slot="suffix"></ha-icon
                ></paper-input>
                <paper-input
                  placeholder="Nazwa bazy"
                  no-label-float=""
                  type="text"
                  id="db_server_name"
                  value="[[dbServerName]]"
                  on-change="_computeDbUrl"
                  ><ha-icon icon="mdi:database-check" slot="suffix"></ha-icon
                ></paper-input>
                <br /><br />
              </div>
              <div class="card-content" style$="[[dbKeepDaysDisplayStyle]]">
                Żeby utrzymać system w dobrej kondycji, codziennie dokładnie o
                godzinie 4:12 rano Asystent usuwa z bazy zdarzenia i stany
                starsze niż <b>określona liczba dni</b> (2 dni dla bazy w
                pamięci urządzenia i domyślnie 10 dla innych lokalizacji).
                <br />
                W tym miejscu możesz określić liczbę dni, których historia ma
                być przechowywana w bazie danych.
                <paper-input
                  id="db_keep_days"
                  type="number"
                  value="[[dbKeepDays]]"
                  on-change="_computeDbUrl"
                  maxlength="4"
                  max="9999"
                  min="1"
                  label-float="Liczba dni historii przechowywanych w bazie"
                  label="Liczba dni historii przechowywanych w bazie"
                >
                  <ha-icon icon="mdi:calendar" slot="suffix"></ha-icon>
                </paper-input>
              </div>
              <div class="card-content">
                [[dbUrl]]
                <br /><br />
                <div class="center-container">
                  <template is="dom-if" if="[[dbConnectionValidating]]">
                    <paper-spinner active=""></paper-spinner>
                  </template>
                  <template is="dom-if" if="[[!dbConnectionValidating]]">
                    <div class="config-invalid">
                      <span class="text">
                        [[validationError]]
                      </span>
                    </div>
                    <ha-call-service-button
                      class="warning"
                      hass="[[hass]]"
                      domain="ais_files"
                      service="check_db_connection"
                      service-data="[[_addAisDbConnectionData()]]"
                      >[[dbConnectionInfoButton]]
                    </ha-call-service-button>
                  </template>
                </div>
                <div>
                  * po zmianie połączenia z bazą wymagany jest restart systemu.
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,logLevel:{type:String,value:"info"},logDrive:{type:String,value:"-"},logError:{type:String,computed:"_computeLogsSettings(hass)"},logRotating:Number,logIconAnimationStyle:String,dbIconAnimationStyle:String,usbDrives:{type:Object,computed:"_computeUsbDrives(hass)"},dbDrives:{type:Object,computed:"_computeDbDrives(hass)"},dbConnectionValidating:{type:Boolean,value:!1},dbConnectionInfoButton:{type:String,computed:"_computeDbConnectionSettings(hass)"},validationError:String,logModeInfo:String,dbUrl:String,dbConectionDisplayStyle:String,dbFileDisplayStyle:String,dbKeepDaysDisplayStyle:String,dbDrive:String,dbEngine:String,dbUser:String,dbPassword:String,dbServerIp:String,dbServerName:String,dbKeepDays:Number}}ready(){super.ready(),this.hass.callService("ais_files","get_db_log_settings_info"),this._computeLogsSettings(this.hass)}computeClasses(e){return e?"content":"content narrow"}_computeUsbDrives(e){return e.states["input_select.ais_usb_flash_drives"]}_computeLogsSettings(e){const t=e.states["sensor.ais_logs_settings_info"],i=t.attributes;this.logDrive=i.logDrive,this.logLevel=i.logLevel,this.logRotating=i.logRotating,t.state>0?"debug"===this.logLevel?this.logIconAnimationStyle="animation: pulseRed 2s infinite;":"info"===this.logLevel?this.logIconAnimationStyle="animation: pulseRed 4s infinite;":"info"===this.logLevel?this.logIconAnimationStyle="animation: pulse 5s infinite;":"warn"===this.logLevel?this.logIconAnimationStyle="animation: pulse 6s infinite;":"warning"===this.logLevel?this.logIconAnimationStyle="animation: pulse 7s infinite;":"error"===this.logLevel?this.logIconAnimationStyle="animation: pulse 8s infinite;":"fatal"===this.logLevel?this.logIconAnimationStyle="animation: pulse 9s infinite;":"critical"===this.logLevel&&(this.logIconAnimationStyle="animation: pulse 10s infinite;"):this.logIconAnimationStyle="";let a="";return i.logError&&(a=i.logError),"debug"===this.logLevel&&t.state&&(a+=" Logowanie w trybie debug generuje duże ilości logów i obciąża system. Używaj go tylko na czas diagnozowania problemu. "),a}logDriveChanged(e){this.logDrive=e.detail.value,"-"!==this.logDrive?this.logModeInfo="Zapis logów do pliku /dyski-wymienne/"+this.logDrive+"/ais.log":this.logModeInfo="Zapis logów do pliku wyłączony ",this.hass.callService("ais_files","change_logger_settings",{log_drive:this.logDrive,log_level:this.logLevel,log_rotating:String(this.logRotating)})}logLevelChanged(e){this.logLevel=e.detail.value,this.logModeInfo="Poziom logów: "+this.logLevel,this.hass.callService("ais_files","change_logger_settings",{log_drive:this.logDrive,log_level:this.logLevel,log_rotating:String(this.logRotating)})}logRotatingDaysChanged(e){this.logRotating=Number(e.target.value),1===this.logRotating?this.logModeInfo="Rotacja logów codziennie.":this.logModeInfo="Rotacja logów co "+this.logRotating+" dni.",this.hass.callService("ais_files","change_logger_settings",{log_drive:this.logDrive,log_level:this.logLevel,log_rotating:String(this.logRotating)})}_computeDbConnectionSettings(e){const t=e.states["sensor.ais_db_connection_info"],i=t.attributes;this.validationError=i.errorInfo,this.dbEngine=i.dbEngine,this.dbEngine||(this.dbEngine="-"),this.dbDrive||(this.dbDrive=i.dbDrive),this.dbUrl=i.dbUrl,this.dbPassword=i.dbPassword,this.dbUser=i.dbUser,this.dbServerIp=i.dbServerIp,this.dbServerName=i.dbServerName,this.dbKeepDays=i.dbKeepDays;let a="";return"no_db_url_saved"===t.state?(a="Sprawdź połączenie",this.dbIconAnimationStyle=""):"db_url_saved"===t.state?(a="Usuń polączenie",this.dbIconAnimationStyle="animation: pulse 6s infinite;"):"db_url_not_valid"===t.state?(a="Sprawdź połączenie",this.dbIconAnimationStyle="animation: pulseRed 3s infinite;"):"db_url_valid"===t.state&&(a="Zapisz połączenie",this.dbIconAnimationStyle="animation: pulse 4s infinite;"),this.dbConnectionValidating=!1,this._doComputeDbUrl(!1),a}_addAisDbConnectionData(){return{buttonClick:!0}}_computeDbDrives(e){return e.states["input_select.ais_usb_flash_drives"]}_doComputeDbUrl(e){let t="";if("-"===this.dbEngine)this.dbConectionDisplayStyle="display: none",this.dbFileDisplayStyle="display: none",this.dbKeepDaysDisplayStyle="display: none",t="";else if("SQLite (file)"===this.dbEngine)this.dbConectionDisplayStyle="display: none",this.dbFileDisplayStyle="",this.dbKeepDaysDisplayStyle="",t="sqlite://///data/data/pl.sviete.dom/files/home/dom/dyski-wymienne/"+this.dbDrive+"/ais.db",e&&(this.dbKeepDays=this.shadowRoot.getElementById("db_keep_days").value);else if("SQLite (memory)"===this.dbEngine)this.dbConectionDisplayStyle="display: none",this.dbFileDisplayStyle="display: none",this.dbKeepDaysDisplayStyle="display: none",t="sqlite:///:memory:";else{this.dbFileDisplayStyle="display: none",this.dbConectionDisplayStyle="",this.dbKeepDaysDisplayStyle="",e&&(this.dbPassword=this.shadowRoot.getElementById("db_password").value,this.dbUser=this.shadowRoot.getElementById("db_user").value,this.dbServerIp=this.shadowRoot.getElementById("db_server_ip").value,this.dbServerName=this.shadowRoot.getElementById("db_server_name").value,this.dbKeepDays=this.shadowRoot.getElementById("db_keep_days").value);let i="";(this.dbUser||this.dbPassword)&&(i=this.dbUser+":"+this.dbPassword+"@"),"MariaDB"===this.dbEngine?t="mysql+pymysql://"+i+this.dbServerIp+"/"+this.dbServerName+"?charset=utf8mb4":"MySQL"===this.dbEngine?t="mysql://"+i+this.dbServerIp+"/"+this.dbServerName+"?charset=utf8mb4":"PostgreSQL"===this.dbEngine&&(t="postgresql://"+i+this.dbServerIp+"/"+this.dbServerName)}this.dbUrl=t}_computeDbUrl(){this._doComputeDbUrl(!0),this.hass.callService("ais_files","check_db_connection",{buttonClick:!1,dbEngine:this.dbEngine,dbDrive:this.dbDrive,dbUrl:this.dbUrl,dbPassword:this.dbPassword,dbUser:this.dbUser,dbServerIp:this.dbServerIp,dbServerName:this.dbServerName,dbKeepDays:this.dbKeepDays,errorInfo:""})}dbDriveChanged(e){const t=e.detail.value;this.dbDrive=t,this._computeDbUrl()}dbEngineChanged(e){const t=e.detail.value;this.dbEngine=t,this._computeDbUrl()}}customElements.define("ha-config-ais-dom-config-logs",n)},61578:(e,t,i)=>{"use strict";i.r(t);i(53268),i(12730);var a=i(50856),r=i(28426),n=(i(60010),i(38353),i(63081),i(15652)),o=(i(53973),i(89194),i(22098),i(43408)),s=i(47181);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(a){t.forEach((function(t){var r=t.placement;if(t.kind===a&&("static"===r||"prototype"===r)){var n="static"===r?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var a=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],a=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,r);i.push(t.element),i.push.apply(i,t.extras),a.push.apply(a,t.finishers)}),this),!t)return{elements:i,finishers:a};var n=this.decorateConstructor(i,t);return a.push.apply(a,n.finishers),n.finishers=a,n},addElementPlacement:function(e,t,i){var a=t[e.placement];if(!i&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var i=[],a=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&a.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:a,extras:i}},decorateConstructor:function(e,t){for(var i=[],a=t.length-1;a>=0;a--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[a])(r)||r);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:a,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var a=(0,t[i])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function c(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var a=i.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,a=new Array(t);i<t;i++)a[i]=e[i];return a}function b(e,t,i){return(b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var a=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(a){var r=Object.getOwnPropertyDescriptor(a,t);return r.get?r.get.call(i):r.value}})(e,t,i||e)}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let g=function(e,t,i,a){var r=l();if(a)for(var n=0;n<a.length;n++)r=a[n](r);var o=t((function(e){r.initializeInstanceElements(e,s.elements)}),i),s=r.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},a=0;a<e.length;a++){var r,n=e[a];if("method"===n.kind&&(r=t.find(i)))if(m(n.descriptor)||m(r.descriptor)){if(p(n)||p(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(p(n)){if(p(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}d(n,r)}else t.push(n)}return t}(o.d.map(c)),e);return r.initializeClassElements(o.F,s.elements),r.runClassFinishers(o.F,s.finishers)}(null,(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_localHooks",value:void 0},{kind:"get",static:!0,key:"properties",value:function(){return{hass:{},_localHooks:{}}}},{kind:"method",key:"connectedCallback",value:function(){b(y(a.prototype),"connectedCallback",this).call(this),this._fetchData()}},{kind:"method",key:"render",value:function(){return n.dy`
      ${this.renderStyle()}
      <ha-card header="Wywołania zwrotne HTTP">
        <div class="card-content">
          Wywołania zwrotne HTTP (Webhook) używane są do udostępniania
          powiadomień o zdarzeniach. Wszystko, co jest skonfigurowane do
          uruchamiania przez wywołanie zwrotne, ma publicznie dostępny unikalny
          adres URL, aby umożliwić wysyłanie danych do Asystenta domowego z
          dowolnego miejsca. ${this._renderBody()}

          <div class="footer">
            <a href="https://www.ai-speaker.com/" target="_blank">
              Dowiedz się więcej o zwrotnym wywołaniu HTTP.
            </a>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_renderBody",value:function(){return this._localHooks?1===this._localHooks.length?n.dy`
        <div class="body-text">
          Wygląda na to, że nie masz jeszcze zdefiniowanych żadnych wywołań
          zwrotnych. Rozpocznij od skonfigurowania
          <a href="/config/integrations">
            integracji opartej na wywołaniu zwrotnym
          </a>
          lub przez tworzenie
          <a href="/config/automation/new"> automatyzacji typu webhook </a>.
        </div>
      `:this._localHooks.map((e=>n.dy`
        ${"aisdomprocesscommandfromframe"===e.webhook_id?n.dy` <div></div> `:n.dy`
              <div class="webhook" .entry="${e}">
                <paper-item-body two-line>
                  <div>
                    ${e.name}
                    ${e.domain===e.name.toLowerCase()?"":` (${e.domain})`}
                  </div>
                  <div secondary>${e.webhook_id}</div>
                </paper-item-body>
                <mwc-button @click="${this._handleManageButton}">
                  Pokaż
                </mwc-button>
              </div>
            `}
      `)):n.dy` <div class="body-text">Pobieranie…</div> `}},{kind:"method",key:"_showDialog",value:function(e){const t=this._localHooks.find((t=>t.webhook_id===e));var a,r;a=this,r={webhook:t},(0,s.B)(a,"show-dialog",{dialogTag:"dialog-manage-ais-cloudhook",dialogImport:()=>i.e(4795).then(i.bind(i,96519)),dialogParams:r})}},{kind:"method",key:"_handleManageButton",value:function(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}},{kind:"method",key:"_fetchData",value:async function(){this._localHooks=await(0,o.H)(this.hass)}},{kind:"method",key:"renderStyle",value:function(){return n.dy`
      <style>
        .body-text {
          padding: 8px 0;
        }
        .webhook {
          display: flex;
          padding: 4px 0;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding-top: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}}]}}),n.oi);customElements.define("ais-webhooks",g);i(43709),i(21157),i(76111);var v=i(83599),w=i(91168);class k extends r.H3{static get template(){return a.d`
      <style include="iron-flex iron-flex-alignment"></style>

      [[_secondsToDuration(timeRemaining)]]
    `}static get properties(){return{hass:Object,stateObj:{type:Object,observer:"stateObjChanged"},timeRemaining:Number,inDialog:{type:Boolean,value:!1}}}connectedCallback(){super.connectedCallback(),this.startInterval(this.stateObj)}disconnectedCallback(){super.disconnectedCallback(),this.clearInterval()}stateObjChanged(e){this.startInterval(e)}clearInterval(){this._updateRemaining&&(clearInterval(this._updateRemaining),this._updateRemaining=null)}startInterval(e){this.clearInterval(),this.calculateRemaining(e),"active"===e.state&&(this._updateRemaining=setInterval((()=>this.calculateRemaining(this.stateObj)),1e3))}calculateRemaining(e){this.timeRemaining=(0,v.m)(e)}_secondsToDuration(e){return(0,w.Z)(e)}}customElements.define("ais-timer",k);class _ extends r.H3{static get template(){return a.d`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }
        a {
          color: var(--primary-color);
        }
        span.pin {
          color: var(--primary-color);
          font-size: 2em;
        }
        .border {
          margin-bottom: 12px;
          border-bottom: 2px solid rgba(0, 0, 0, 0.11);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        ha-card > div#ha-switch-id {
          margin: -4px 0;
          position: absolute;
          right: 8px;
          top: 32px;
        }
        .card-actions a {
          text-decoration: none;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Zdalny dostęp</span>
            <span slot="introduction"
              >W tej sekcji możesz skonfigurować zdalny dostęp do bramki</span
            >
            <ha-card header="Szyfrowany tunel">
              <div id="ha-switch-id">
                <ha-switch
                  checked="{{remoteConnected}}"
                  on-change="changeRemote"
                ></ha-switch>
              </div>
              <div class="card-content">
                Tunel zapewnia bezpieczne zdalne połączenie z Twoim urządzeniem
                kiedy jesteś z dala od domu. Twoja bramka dostępna
                [[remoteInfo]] z Internetu pod adresem
                <a href="[[remoteDomain]]" target="_blank">[[remoteDomain]]</a>.
                <div class="center-container border" style="height: 320px;">
                  <div style="text-align: center; margin-top: 10px;">
                    <img src="/local/dom_access_code.png" />
                  </div>
                  Zeskanuj kod QR za pomocą aplikacji na telefonie.
                </div>
              </div>
              <div class="card-content" style="text-align:center;">
                <svg style="width:48px;height:48px" viewBox="0 0 24 24">
                  <path
                    fill="#929395"
                    d="M1,11H6L3.5,8.5L4.92,7.08L9.84,12L4.92,16.92L3.5,15.5L6,13H1V11M8,0H16L16.83,5H17A2,2 0 0,1 19,7V17C19,18.11 18.1,19 17,19H16.83L16,24H8L7.17,19H7C6.46,19 6,18.79 5.62,18.44L7.06,17H17V7H7.06L5.62,5.56C6,5.21 6.46,5 7,5H7.17L8,0Z"
                  />
                </svg>
                <br />
                <template is="dom-if" if="[[!gatePinPairing]]">
                  [[gatePinPairingInfo]]
                  <br />
                  <mwc-button on-click="enableGatePariringByPin"
                    >Generuj kod PIN</mwc-button
                  >
                </template>
                <template is="dom-if" if="[[gatePinPairing]]">
                  <span class="pin">[[gatePin]]</span><br />
                  [[gatePinPairingInfo]]
                  <template is="dom-if" if="[[stateObj]]">
                    <ais-timer
                      hass="[[hass]]"
                      state-obj="[[stateObj]]"
                      in-dialog
                    ></ais-timer>
                  </template>
                </template>
              </div>
              <div class="card-actions">
                <a
                  href="https://www.ai-speaker.com/docs/ais_bramka_remote_www_index"
                  target="_blank"
                >
                  <mwc-button>Dowiedz się jak to działa</mwc-button>
                </a>
              </div>
            </ha-card>

            <ais-webhooks hass="[[hass]]"></ais-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,remoteInfo:{type:String,value:"jest"},remoteDomain:{type:String,computed:"_computeRemoteDomain(hass)"},remoteConnected:{type:Boolean,computed:"_computeRremoteConnected(hass)"},gatePinPairingInfo:{type:String},gatePin:{type:String},gatePinPairing:{type:Boolean,computed:"_computeGatePinPairing(hass)"},stateObj:{type:Object,computed:"_computeStateObj(hass)"}}}_computeRemoteDomain(e){return"https://"+e.states["sensor.ais_secure_android_id_dom"].state+".paczka.pro"}_computeStateObj(e){return e.states["timer.ais_dom_pin_join"]}_computeGatePinPairing(e){return"active"===e.states["timer.ais_dom_pin_join"].state?(this.gatePin=e.states["sensor.gate_pairing_pin"].state,this.gatePinPairingInfo="PIN aktywny przez dwie munuty:",!0):(this.gatePin="",this.gatePinPairingInfo="Włącz parowanie z bramką za pomocą PIN",!1)}_computeRremoteConnected(e){return"on"===e.states["input_boolean.ais_remote_access"].state?(this.remoteInfo="jest",!0):(this.remoteInfo="będzie",!1)}changeRemote(){this.hass.callService("input_boolean","toggle",{entity_id:"input_boolean.ais_remote_access"})}enableGatePariringByPin(){this.hass.callService("ais_cloud","enable_gate_pairing_by_pin")}}customElements.define("ha-config-ais-dom-config-remote",_)}}]);
//# sourceMappingURL=chunk.28981c6a4b48282e4036.js.map