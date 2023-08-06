/*! For license information please see chunk.881b446ba2282e39d5ee.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[76],{44285:(e,t,i)=>{"use strict";i(43437);var r=i(9672),o=i(50856),s=i(42687);(0,r.k)({_template:o.d`
    <style>
      :host {
        display: inline-block;
        overflow: hidden;
        position: relative;
      }

      #baseURIAnchor {
        display: none;
      }

      #sizedImgDiv {
        position: absolute;
        top: 0px;
        right: 0px;
        bottom: 0px;
        left: 0px;

        display: none;
      }

      #img {
        display: block;
        width: var(--iron-image-width, auto);
        height: var(--iron-image-height, auto);
      }

      :host([sizing]) #sizedImgDiv {
        display: block;
      }

      :host([sizing]) #img {
        display: none;
      }

      #placeholder {
        position: absolute;
        top: 0px;
        right: 0px;
        bottom: 0px;
        left: 0px;

        background-color: inherit;
        opacity: 1;

        @apply --iron-image-placeholder;
      }

      #placeholder.faded-out {
        transition: opacity 0.5s linear;
        opacity: 0;
      }
    </style>

    <a id="baseURIAnchor" href="#"></a>
    <div id="sizedImgDiv" role="img" hidden$="[[_computeImgDivHidden(sizing)]]" aria-hidden$="[[_computeImgDivARIAHidden(alt)]]" aria-label$="[[_computeImgDivARIALabel(alt, src)]]"></div>
    <img id="img" alt$="[[alt]]" hidden$="[[_computeImgHidden(sizing)]]" crossorigin$="[[crossorigin]]" on-load="_imgOnLoad" on-error="_imgOnError">
    <div id="placeholder" hidden$="[[_computePlaceholderHidden(preload, fade, loading, loaded)]]" class$="[[_computePlaceholderClassName(preload, fade, loading, loaded)]]"></div>
`,is:"iron-image",properties:{src:{type:String,value:""},alt:{type:String,value:null},crossorigin:{type:String,value:null},preventLoad:{type:Boolean,value:!1},sizing:{type:String,value:null,reflectToAttribute:!0},position:{type:String,value:"center"},preload:{type:Boolean,value:!1},placeholder:{type:String,value:null,observer:"_placeholderChanged"},fade:{type:Boolean,value:!1},loaded:{notify:!0,readOnly:!0,type:Boolean,value:!1},loading:{notify:!0,readOnly:!0,type:Boolean,value:!1},error:{notify:!0,readOnly:!0,type:Boolean,value:!1},width:{observer:"_widthChanged",type:Number,value:null},height:{observer:"_heightChanged",type:Number,value:null}},observers:["_transformChanged(sizing, position)","_loadStateObserver(src, preventLoad)"],created:function(){this._resolvedSrc=""},_imgOnLoad:function(){this.$.img.src===this._resolveSrc(this.src)&&(this._setLoading(!1),this._setLoaded(!0),this._setError(!1))},_imgOnError:function(){this.$.img.src===this._resolveSrc(this.src)&&(this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",this._setLoading(!1),this._setLoaded(!1),this._setError(!0))},_computePlaceholderHidden:function(){return!this.preload||!this.fade&&!this.loading&&this.loaded},_computePlaceholderClassName:function(){return this.preload&&this.fade&&!this.loading&&this.loaded?"faded-out":""},_computeImgDivHidden:function(){return!this.sizing},_computeImgDivARIAHidden:function(){return""===this.alt?"true":void 0},_computeImgDivARIALabel:function(){return null!==this.alt?this.alt:""===this.src?"":this._resolveSrc(this.src).replace(/[?|#].*/g,"").split("/").pop()},_computeImgHidden:function(){return!!this.sizing},_widthChanged:function(){this.style.width=isNaN(this.width)?this.width:this.width+"px"},_heightChanged:function(){this.style.height=isNaN(this.height)?this.height:this.height+"px"},_loadStateObserver:function(e,t){var i=this._resolveSrc(e);i!==this._resolvedSrc&&(this._resolvedSrc="",this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",""===e||t?(this._setLoading(!1),this._setLoaded(!1),this._setError(!1)):(this._resolvedSrc=i,this.$.img.src=this._resolvedSrc,this.$.sizedImgDiv.style.backgroundImage='url("'+this._resolvedSrc+'")',this._setLoading(!0),this._setLoaded(!1),this._setError(!1)))},_placeholderChanged:function(){this.$.placeholder.style.backgroundImage=this.placeholder?'url("'+this.placeholder+'")':""},_transformChanged:function(){var e=this.$.sizedImgDiv.style,t=this.$.placeholder.style;e.backgroundSize=t.backgroundSize=this.sizing,e.backgroundPosition=t.backgroundPosition=this.sizing?this.position:"",e.backgroundRepeat=t.backgroundRepeat=this.sizing?"no-repeat":""},_resolveSrc:function(e){var t=(0,s.Kk)(e,this.$.baseURIAnchor.href);return t.length>=2&&"/"===t[0]&&"/"!==t[1]&&(t=(location.origin||location.protocol+"//"+location.host)+t),t}})},81471:(e,t,i)=>{"use strict";i.d(t,{$:()=>n});var r=i(94707);class o{constructor(e){this.classes=new Set,this.changed=!1,this.element=e;const t=(e.getAttribute("class")||"").split(/\s+/);for(const i of t)this.classes.add(i)}add(e){this.classes.add(e),this.changed=!0}remove(e){this.classes.delete(e),this.changed=!0}commit(){if(this.changed){let e="";this.classes.forEach((t=>e+=t+" ")),this.element.setAttribute("class",e)}}}const s=new WeakMap,n=(0,r.XM)((e=>t=>{if(!(t instanceof r._l)||t instanceof r.sL||"class"!==t.committer.name||t.committer.parts.length>1)throw new Error("The `classMap` directive must be used in the `class` attribute and must be the only part in the attribute.");const{committer:i}=t,{element:n}=i;let a=s.get(t);void 0===a&&(n.setAttribute("class",i.strings.join(" ")),s.set(t,a=new Set));const l=n.classList||new o(n);a.forEach((t=>{t in e||(l.remove(t),a.delete(t))}));for(const r in e){const t=e[r];t!=a.has(r)&&(t?(l.add(r),a.add(r)):(l.remove(r),a.delete(r)))}"function"==typeof l.commit&&l.commit()}))},47181:(e,t,i)=>{"use strict";i.d(t,{B:()=>r});const r=(e,t,i,r)=>{r=r||{},i=null==i?{}:i;const o=new Event(t,{bubbles:void 0===r.bubbles||r.bubbles,cancelable:Boolean(r.cancelable),composed:void 0===r.composed||r.composed});return o.detail=i,e.dispatchEvent(o),o}},52003:(e,t,i)=>{"use strict";i.d(t,{F:()=>r,C:()=>o});const r=async(e,t,r=!1)=>{if(!e.parentNode)throw new Error("Cannot setup Leaflet map on disconnected element");const o=(await i.e(6567).then(i.t.bind(i,70208,7))).default;o.Icon.Default.imagePath="/static/images/leaflet/images/",r&&await i.e(1294).then(i.t.bind(i,27716,7));const n=o.map(e),a=document.createElement("link");a.setAttribute("href","/static/images/leaflet/leaflet.css"),a.setAttribute("rel","stylesheet"),e.parentNode.appendChild(a),n.setView([52.3731339,4.8903147],13);return[n,o,s(o,Boolean(t)).addTo(n)]},o=(e,t,i,r)=>(t.removeLayer(i),(i=s(e,r)).addTo(t),i),s=(e,t)=>e.tileLayer(`https://{s}.basemaps.cartocdn.com/${t?"dark_all":"light_all"}/{z}/{x}/{y}${e.Browser.retina?"@2x.png":".png"}`,{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20})},58831:(e,t,i)=>{"use strict";i.d(t,{M:()=>r});const r=e=>e.substr(0,e.indexOf("."))},38346:(e,t,i)=>{"use strict";i.d(t,{D:()=>r});const r=(e,t,i=!1)=>{let r;return function(...o){const s=this,n=i&&!r;clearTimeout(r),r=setTimeout((()=>{r=null,i||e.apply(s,o)}),t),n&&e.apply(s,o)}}},73589:(e,t,i)=>{"use strict";i.d(t,{Z:()=>o});const r=e=>{const t=parseFloat(e);if(isNaN(t))throw new Error(e+" is not a number");return t};function o(e){if(!e)return null;try{if(e.endsWith("%"))return{w:100,h:r(e.substr(0,e.length-1))};const t=e.replace(":","x").split("x");return 0===t.length?null:1===t.length?{w:r(t[0]),h:1}:{w:r(t[0]),h:r(t[1])}}catch(t){}return null}},11052:(e,t,i)=>{"use strict";i.d(t,{I:()=>s});var r=i(76389),o=i(47181);const s=(0,r.o)((e=>class extends e{fire(e,t,i){return i=i||{},(0,o.B)(i.node||this,e,t,i)}}))},60076:(e,t,i)=>{"use strict";i.r(t);var r=i(15652),o=i(81471),s=i(52003),n=i(58831),a=i(22311),l=i(91741),c=i(38346),d=i(73589),h=(i(22098),i(10983),i(58763)),u=(i(73085),i(64588)),f=i(54845),p=i(90271);function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var s="static"===o?e:i;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!v(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,s=o.length-1;s>=0;s--){var n=t[e.placement];n.splice(n.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var n=0;n<e.length-1;n++)for(var a=n+1;a<e.length;a++)if(e[n].key===e[a].key&&e[n].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[n].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=b(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:k(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=k(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function g(e){var t,i=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function v(e){return e.decorators&&e.decorators.length}function _(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function k(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function b(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function E(e,t,i){return(E="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function C(e){return(C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var o=m();if(r)for(var s=0;s<r.length;s++)o=r[s](o);var n=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var o,s=e[r];if("method"===s.kind&&(o=t.find(i)))if(_(s.descriptor)||_(o.descriptor)){if(v(s)||v(o))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");o.descriptor=s.descriptor}else{if(v(s)){if(v(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");o.decorators=s.decorators}y(s,o)}else t.push(s)}return t}(n.d.map(g)),e);o.initializeClassElements(n.F,a.elements),o.runClassFinishers(n.F,a.finishers)}([(0,r.Mo)("hui-map-card")],(function(e,t){class m extends t{constructor(...t){super(...t),e(this)}}return{F:m,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([i.e(1041),i.e(8374),i.e(1409),i.e(3648),i.e(6087),i.e(5328),i.e(1685),i.e(4535),i.e(6902),i.e(5212)]).then(i.bind(i,44446)),document.createElement("hui-map-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,i){return{type:"map",entities:(0,u.j)(e,2,t,i,["device_tracker"])}}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"isPanel",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"editMode",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)()],key:"_history",value:void 0},{kind:"field",key:"_date",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"_config",value:void 0},{kind:"field",key:"_configEntities",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"field",key:"_leafletMap",value:void 0},{kind:"field",key:"_tileLayer",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"field",key:"_debouncedResizeListener",value(){return(0,c.D)((()=>{this.isConnected&&this._leafletMap&&this._leafletMap.invalidateSize()}),250,!1)}},{kind:"field",key:"_mapItems",value:()=>[]},{kind:"field",key:"_mapZones",value:()=>[]},{kind:"field",key:"_mapPaths",value:()=>[]},{kind:"field",key:"_colorDict",value:()=>({})},{kind:"field",key:"_colorIndex",value:()=>0},{kind:"field",key:"_colors",value:()=>["#0288D1","#00AA00","#984ea3","#00d2d5","#ff7f00","#af8d00","#7f80cd","#b3e900","#c42e60","#a65628","#f781bf","#8dd3c7"]},{kind:"method",key:"setConfig",value:function(e){if(!e)throw new Error("Error in card configuration.");if(!e.entities&&!e.geo_location_sources)throw new Error("Either entities or geo_location_sources must be defined");if(e.entities&&!Array.isArray(e.entities))throw new Error("Entities need to be an array");if(e.geo_location_sources&&!Array.isArray(e.geo_location_sources))throw new Error("Geo_location_sources needs to be an array");this._config=e,this._configEntities=e.entities?(0,p.A)(e.entities):[],this._cleanupHistory()}},{kind:"method",key:"getCardSize",value:function(){var e;if(!(null===(e=this._config)||void 0===e?void 0:e.aspect_ratio))return 7;const t=(0,d.Z)(this._config.aspect_ratio),i=t&&t.w>0&&t.h>0?""+(100*t.h/t.w).toFixed(2):"100";return 1+Math.floor(Number(i)/25)||3}},{kind:"method",key:"connectedCallback",value:function(){E(C(m.prototype),"connectedCallback",this).call(this),this._attachObserver(),this.hasUpdated&&this.loadMap()}},{kind:"method",key:"disconnectedCallback",value:function(){E(C(m.prototype),"disconnectedCallback",this).call(this),this._leafletMap&&(this._leafletMap.remove(),this._leafletMap=void 0,this.Leaflet=void 0),this._resizeObserver&&this._resizeObserver.unobserve(this._mapEl)}},{kind:"method",key:"render",value:function(){return this._config?r.dy`
      <ha-card id="card" .header=${this._config.title}>
        <div id="root">
          <div
            id="map"
            class=${(0,o.$)({dark:!0===this._config.dark_mode})}
          ></div>
          <ha-icon-button
            @click=${this._fitMap}
            tabindex="0"
            icon="hass:image-filter-center-focus"
            title="Reset focus"
          ></ha-icon-button>
        </div>
      </ha-card>
    `:r.dy``}},{kind:"method",key:"shouldUpdate",value:function(e){if(!e.has("hass")||e.size>1)return!0;const t=e.get("hass");if(!t||!this._configEntities)return!0;if(t.themes.darkMode!==this.hass.themes.darkMode)return!0;for(const i of this._configEntities)if(t.states[i.entity]!==this.hass.states[i.entity])return!0;return!1}},{kind:"method",key:"firstUpdated",value:function(e){E(C(m.prototype),"firstUpdated",this).call(this,e),this.isConnected&&this.loadMap();const t=this.shadowRoot.getElementById("root");if(!this._config||this.isPanel||!t)return;if(this._attachObserver(),!this._config.aspect_ratio)return void(t.style.paddingBottom="100%");const i=(0,d.Z)(this._config.aspect_ratio);t.style.paddingBottom=i&&i.w>0&&i.h>0?(100*i.h/i.w).toFixed(2)+"%":t.style.paddingBottom="100%"}},{kind:"method",key:"updated",value:function(e){var t;if((e.has("hass")||e.has("_history"))&&(this._drawEntities(),this._fitMap()),e.has("hass")){const t=e.get("hass");t&&t.themes.darkMode!==this.hass.themes.darkMode&&this._replaceTileLayer()}if(e.has("_config")&&void 0!==e.get("_config")&&this.updateMap(e.get("_config")),this._config.hours_to_show&&(null===(t=this._configEntities)||void 0===t?void 0:t.length)){const t=6e4;(e.has("_config")||Date.now()-this._date.getTime()>=t)&&this._getHistory()}}},{kind:"get",key:"_mapEl",value:function(){return this.shadowRoot.getElementById("map")}},{kind:"method",key:"loadMap",value:async function(){var e;[this._leafletMap,this.Leaflet,this._tileLayer]=await(0,s.F)(this._mapEl,null!==(e=this._config.dark_mode)&&void 0!==e?e:this.hass.themes.darkMode),this._drawEntities(),this._leafletMap.invalidateSize(),this._fitMap()}},{kind:"method",key:"_replaceTileLayer",value:function(){var e;const t=this._leafletMap,i=this._config,r=this.Leaflet;t&&i&&r&&this._tileLayer&&(this._tileLayer=(0,s.C)(r,t,this._tileLayer,null!==(e=this._config.dark_mode)&&void 0!==e?e:this.hass.themes.darkMode))}},{kind:"method",key:"updateMap",value:function(e){const t=this._leafletMap,i=this._config,r=this.Leaflet;t&&i&&r&&this._tileLayer&&(this._config.dark_mode!==e.dark_mode&&this._replaceTileLayer(),i.entities===e.entities&&i.geo_location_sources===e.geo_location_sources||this._drawEntities(),t.invalidateSize(),this._fitMap())}},{kind:"method",key:"_fitMap",value:function(){if(!(this._leafletMap&&this.Leaflet&&this._config&&this.hass))return;const e=this._config.default_zoom;if(0===this._mapItems.length)return void this._leafletMap.setView(new this.Leaflet.LatLng(this.hass.config.latitude,this.hass.config.longitude),e||14);const t=this.Leaflet.featureGroup(this._mapItems).getBounds();this._leafletMap.fitBounds(t.pad(.5)),e&&this._leafletMap.getZoom()>e&&this._leafletMap.setZoom(e)}},{kind:"method",key:"_getColor",value:function(e){let t;return this._colorDict[e]?t=this._colorDict[e]:(t=this._colors[this._colorIndex],this._colorIndex=(this._colorIndex+1)%this._colors.length,this._colorDict[e]=t),t}},{kind:"method",key:"_drawEntities",value:function(){const e=this.hass,t=this._leafletMap,i=this._config,r=this.Leaflet;if(!(e&&t&&i&&r))return;this._mapItems&&this._mapItems.forEach((e=>e.remove()));const o=this._mapItems=[];this._mapZones&&this._mapZones.forEach((e=>e.remove()));const s=this._mapZones=[];this._mapPaths&&this._mapPaths.forEach((e=>e.remove()));const c=this._mapPaths=[],d=this._configEntities.concat();if(i.geo_location_sources){const t=i.geo_location_sources.includes("all");for(const r of Object.keys(e.states)){const o=e.states[r];"geo_location"===(0,n.M)(r)&&(t||i.geo_location_sources.includes(o.attributes.source))&&d.push({entity:r})}}if(this._config.hours_to_show&&this._history)for(const n of this._history){if((null==n?void 0:n.length)<=1)continue;const e=n[0].entity_id,t=n.reduce(((e,t)=>{const i=t.attributes.latitude,r=t.attributes.longitude;return i&&r&&e.push([i,r]),e}),[]);for(let i=0;i<t.length-1;i++){const o=.2+i*(.8/(t.length-2));c.push(r.circleMarker(t[i],{radius:3,color:this._getColor(e),opacity:o,interactive:!1}));const s=[t[i],t[i+1]];c.push(r.polyline(s,{color:this._getColor(e),opacity:o,interactive:!1}))}}for(const n of d){const t=n.entity,i=e.states[t];if(!i)continue;const c=(0,l.C)(i),{latitude:d,longitude:h,passive:u,icon:f,radius:p,entity_picture:m,gps_accuracy:g}=i.attributes;if(!d||!h)continue;if("zone"===(0,a.N)(i)){if(u)continue;let e="";if(f){const t=document.createElement("ha-icon");t.setAttribute("icon",f),e=t.outerHTML}else{const t=document.createElement("span");t.innerHTML=c,e=t.outerHTML}s.push(r.marker([d,h],{icon:r.divIcon({html:e,iconSize:[24,24],className:this._config.dark_mode?"dark":!1===this._config.dark_mode?"light":""}),interactive:!1,title:c})),s.push(r.circle([d,h],{interactive:!1,color:"#FF9800",radius:p}));continue}const y=c.split(" ").map((e=>e[0])).join("").substr(0,3);o.push(r.marker([d,h],{icon:r.divIcon({html:`\n              <ha-entity-marker\n                entity-id="${t}"\n                entity-name="${y}"\n                entity-picture="${m||""}"\n                entity-color="${this._getColor(t)}"\n              ></ha-entity-marker>\n            `,iconSize:[48,48],className:""}),title:(0,l.C)(i)})),g&&o.push(r.circle([d,h],{interactive:!1,color:this._getColor(t),radius:g}))}this._mapItems.forEach((e=>t.addLayer(e))),this._mapZones.forEach((e=>t.addLayer(e))),this._mapPaths.forEach((e=>t.addLayer(e)))}},{kind:"method",key:"_attachObserver",value:async function(){this._resizeObserver||(await(0,f.P)(),this._resizeObserver=new ResizeObserver(this._debouncedResizeListener)),this._resizeObserver.observe(this)}},{kind:"method",key:"_getHistory",value:async function(){if(this._date=new Date,!this._configEntities)return;const e=this._configEntities.map((e=>e.entity)).join(","),t=new Date,i=new Date;i.setHours(t.getHours()-this._config.hours_to_show);const r=await(0,h.vq)(this.hass,e,i,t,!1,!1,!1);r.length<1||(this._history=r)}},{kind:"method",key:"_cleanupHistory",value:function(){if(this._history)if(this._config.hours_to_show<=0)this._history=void 0;else{var e;const t=null===(e=this._configEntities)||void 0===e?void 0:e.map((e=>e.entity));this._history=this._history.reduce(((e,i)=>{const r=i[0].entity_id;return(null==t?void 0:t.includes(r))&&e.push(i),e}),[])}}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host([ispanel][editMode]) ha-card {
        height: calc(100% - 51px);
      }

      ha-card {
        overflow: hidden;
        width: 100%;
        height: 100%;
      }

      #map {
        z-index: 0;
        border: none;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: inherit;
      }

      ha-icon-button {
        position: absolute;
        top: 75px;
        left: 3px;
        outline: none;
      }

      #root {
        position: relative;
      }

      :host([ispanel]) #root {
        height: 100%;
      }

      .dark {
        color: #ffffff;
      }

      .light {
        color: #000000;
      }
    `}}]}}),r.oi)},73085:(e,t,i)=>{"use strict";i(44285);var r=i(50856),o=i(28426),s=i(11052);class n extends((0,s.I)(o.H3)){static get template(){return r.d`
      <style include="iron-positioning"></style>
      <style>
        .marker {
          vertical-align: top;
          position: relative;
          display: block;
          margin: 0 auto;
          width: 2.5em;
          text-align: center;
          height: 2.5em;
          line-height: 2.5em;
          font-size: 1.5em;
          border-radius: 50%;
          border: 0.1em solid var(--ha-marker-color, var(--primary-color));
          color: rgb(76, 76, 76);
          background-color: white;
        }
        iron-image {
          border-radius: 50%;
        }
      </style>

      <div class="marker" style$="border-color:{{entityColor}}">
        <template is="dom-if" if="[[entityName]]">[[entityName]]</template>
        <template is="dom-if" if="[[entityPicture]]">
          <iron-image
            sizing="cover"
            class="fit"
            src="[[entityPicture]]"
          ></iron-image>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},entityId:{type:String,value:""},entityName:{type:String,value:null},entityPicture:{type:String,value:null},entityColor:{type:String,value:null}}}ready(){super.ready(),this.addEventListener("click",(e=>this.badgeTap(e)))}badgeTap(e){e.stopPropagation(),this.entityId&&this.fire("hass-more-info",{entityId:this.entityId})}}customElements.define("ha-entity-marker",n)}}]);
//# sourceMappingURL=chunk.881b446ba2282e39d5ee.js.map