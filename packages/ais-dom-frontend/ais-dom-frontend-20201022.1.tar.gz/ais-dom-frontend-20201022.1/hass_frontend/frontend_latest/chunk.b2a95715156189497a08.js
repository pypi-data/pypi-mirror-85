(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6668],{96151:(e,t,r)=>{"use strict";r.d(t,{T:()=>i,y:()=>n});const i=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},n=()=>new Promise((e=>{i(e)}))},34821:(e,t,r)=>{"use strict";r.d(t,{i:()=>y});r(21458);var i=r(60814),n=r(55317),o=r(15652),a=r(87744);r(10983);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function f(e,t,r){return(f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const v=customElements.get("mwc-dialog"),y=(e,t)=>o.dy`
  <span class="header_title">${t}</span>
  <mwc-icon-button
    aria-label=${e.localize("ui.dialogs.generic.close")}
    dialogAction="close"
    class="header_button"
    dir=${(0,a.Zu)(e)}
  >
    <ha-svg-icon .path=${n.r5M}></ha-svg-icon>
  </mwc-icon-button>
`;!function(e,t,r,i){var n=s();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,h.elements)}),r),h=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(u(o.descriptor)||u(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(a.d.map(l)),e);n.initializeClassElements(a.F,h.elements),n.runClassFinishers(a.F,h.finishers)}([(0,o.Mo)("ha-dialog")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"method",key:"scrollToPos",value:function(e,t){this.contentElement.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return o.dy`<slot name="heading">
      ${f(g(r.prototype),"renderHeading",this).call(this)}
    </slot>`}},{kind:"get",static:!0,key:"styles",value:function(){return[i.o,o.iv`
        .mdc-dialog {
          --mdc-dialog-scroll-divider-color: var(--divider-color);
          z-index: var(--dialog-z-index, 7);
        }
        .mdc-dialog__actions {
          justify-content: var(--justify-action-buttons, flex-end);
          padding-bottom: max(env(safe-area-inset-bottom), 8px);
        }
        .mdc-dialog__container {
          align-items: var(--vertial-align-dialog, center);
        }
        .mdc-dialog__title::before {
          display: block;
          height: 20px;
        }
        .mdc-dialog .mdc-dialog__content {
          position: var(--dialog-content-position, relative);
          padding: var(--dialog-content-padding, 20px 24px);
        }
        :host([hideactions]) .mdc-dialog .mdc-dialog__content {
          padding-bottom: max(
            var(--dialog-content-padding, 20px),
            env(safe-area-inset-bottom)
          );
        }
        .mdc-dialog .mdc-dialog__surface {
          position: var(--dialog-surface-position, relative);
          top: var(--dialog-surface-top);
          min-height: var(--mdc-dialog-min-height, auto);
        }
        :host([flexContent]) .mdc-dialog .mdc-dialog__content {
          display: flex;
          flex-direction: column;
        }
        .header_button {
          position: absolute;
          right: 16px;
          top: 10px;
          text-decoration: none;
          color: inherit;
        }
        .header_title {
          margin-right: 40px;
        }
        [dir="rtl"].header_button {
          right: auto;
          left: 16px;
        }
        [dir="rtl"].header_title {
          margin-left: 40px;
          margin-right: 0px;
        }
      `]}}]}}),v)},15327:(e,t,r)=>{"use strict";r.d(t,{eL:()=>i,SN:()=>n,id:()=>o,fg:()=>a,j2:()=>s,JR:()=>l,Y:()=>d,iM:()=>c,Q2:()=>u,Oh:()=>h,vj:()=>p,Gc:()=>m});const i=e=>e.sendMessagePromise({type:"lovelace/resources"}),n=(e,t)=>e.callWS({type:"lovelace/resources/create",...t}),o=(e,t,r)=>e.callWS({type:"lovelace/resources/update",resource_id:t,...r}),a=(e,t)=>e.callWS({type:"lovelace/resources/delete",resource_id:t}),s=e=>e.callWS({type:"lovelace/dashboards/list"}),l=(e,t)=>e.callWS({type:"lovelace/dashboards/create",...t}),d=(e,t,r)=>e.callWS({type:"lovelace/dashboards/update",dashboard_id:t,...r}),c=(e,t)=>e.callWS({type:"lovelace/dashboards/delete",dashboard_id:t}),u=(e,t,r)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:r}),h=(e,t,r)=>e.callWS({type:"lovelace/config/save",url_path:t,config:r}),p=(e,t)=>e.callWS({type:"lovelace/config/delete",url_path:t}),m=(e,t,r)=>e.subscribeEvents((e=>{e.data.url_path===t&&r()}),"lovelace_updated")},96491:(e,t,r)=>{"use strict";r.d(t,{$:()=>s});var i=r(15327),n=r(47512),o=r(4398),a=r(26765);const s=async(e,t,r,s)=>{var l,d,c;const u=await(0,i.j2)(t),h=u.filter((e=>"storage"===e.mode)),p=null===(l=t.panels.lovelace)||void 0===l||null===(d=l.config)||void 0===d?void 0:d.mode;if("storage"!==p&&!h.length)return void(0,n.f)(e,{entities:r,yaml:!0});let m,f=null;if("storage"===p)try{m=await(0,i.Q2)(t.connection,null,!1)}catch(g){}if(!m&&h.length)for(const n of h)try{m=await(0,i.Q2)(t.connection,n.url_path,!1),f=n.url_path;break}catch(g){}m?h.length||(null===(c=m.views)||void 0===c?void 0:c.length)?h.length||1!==m.views.length?(0,o.i)(e,{lovelaceConfig:m,urlPath:f,allowDashboardChange:!0,dashboards:u,viewSelectedCallback:(o,a,l)=>{(0,n.f)(e,{lovelaceConfig:a,saveConfig:async e=>{try{await(0,i.Oh)(t,o,e)}catch{alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[l],entities:r,cardConfig:s})}}):(0,n.f)(e,{lovelaceConfig:m,saveConfig:async e=>{try{await(0,i.Oh)(t,null,e)}catch(g){alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[0],entities:r,cardConfig:s}):(0,a.Ys)(e,{text:"You don't have any Lovelace views, first create a view in Lovelace."}):u.length>h.length?(0,n.f)(e,{entities:r,yaml:!0}):(0,a.Ys)(e,{text:"You don't seem to be in control of any dashboard, please take control first."})}},47512:(e,t,r)=>{"use strict";r.d(t,{f:()=>o});var i=r(47181);const n=()=>Promise.all([r.e(5009),r.e(8426),r.e(3437),r.e(9033),r.e(1572),r.e(486),r.e(9333),r.e(3603),r.e(4582),r.e(3822),r.e(5548),r.e(2390),r.e(6278),r.e(9669),r.e(6369),r.e(768),r.e(8133)]).then(r.bind(r,9444)),o=(e,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"hui-dialog-suggest-card",dialogImport:n,dialogParams:t})}},4398:(e,t,r)=>{"use strict";r.d(t,{i:()=>n});var i=r(47181);const n=(e,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"hui-dialog-select-view",dialogImport:()=>Promise.all([r.e(5009),r.e(8161),r.e(4358),r.e(1458),r.e(9278),r.e(5024)]).then(r.bind(r,9700)),dialogParams:t})}},85494:(e,t,r)=>{"use strict";r.r(t),r.d(t,{HuiDialogWebBrowserAisEditImage:()=>v});var i=r(15652),n=(r(51095),r(55317)),o=r(47181),a=r(34821),s=(r(319),r(11654)),l=r(96491);r(53822),r(74535),r(81303);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}let v=function(e,t,r,i){var n=d();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(p(o.descriptor)||p(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}u(o,n)}else t.push(o)}return t}(a.d.map(c)),e);return n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,i.Mo)("hui-dialog-web-browser-ais-edit-image")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"codeValue",value:()=>""},{kind:"field",decorators:[(0,i.sz)()],key:"selectedElementType",value:()=>""},{kind:"field",decorators:[(0,i.sz)()],key:"selectedEntityId",value:()=>""},{kind:"field",decorators:[(0,i.sz)()],key:"pictureElements",value:()=>[]},{kind:"field",decorators:[(0,i.sz)()],key:"dragCurrentItemIndex",value:()=>-1},{kind:"field",decorators:[(0,i.sz)()],key:"dragItems",value:()=>[]},{kind:"field",decorators:[(0,i.sz)()],key:"dragItemStyle",value:()=>""},{kind:"field",decorators:[(0,i.sz)()],key:"dragActive",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this.codeValue="type: picture-elements\nimage: '/local/img/${this._params.title}'\ntitle: ''\nelements: []",this.selectedElementType="",this.selectedEntityId="",this.pictureElements=[]}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,o.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"_dragStart",value:function(e){isNaN(e.target.id)||void 0!==this.dragItems[e.target.id]&&(this.dragCurrentItemIndex=e.target.id,"touchstart"===e.type?(this.dragItems[this.dragCurrentItemIndex].initialX=e.touches[0].clientX-this.dragItems[this.dragCurrentItemIndex].offsetX,this.dragItems[this.dragCurrentItemIndex].initialY=e.touches[0].clientY-this.dragItems[this.dragCurrentItemIndex].offsetY):(this.dragItems[this.dragCurrentItemIndex].initialX=e.clientX-this.dragItems[this.dragCurrentItemIndex].offsetX,this.dragItems[this.dragCurrentItemIndex].initialY=e.clientY-this.dragItems[this.dragCurrentItemIndex].offsetY),this.dragActive=!0)}},{kind:"method",key:"_dragEnd",value:function(e){this.dragActive&&(this.dragItems[this.dragCurrentItemIndex].initialX=this.dragItems[this.dragCurrentItemIndex].currentX,this.dragItems[this.dragCurrentItemIndex].initialY=this.dragItems[this.dragCurrentItemIndex].currentY,this.dragActive=!1,this.pictureElements[this.dragCurrentItemIndex].style.transform=this.dragItemStyle,this._handleCodeChanged())}},{kind:"method",key:"_getDragStyle",value:function(e){return e===this.dragCurrentItemIndex?"transform: "+this.dragItemStyle:"transform: "+this.dragItems[e].style}},{kind:"method",key:"_drag",value:function(e){if(this.dragActive){let t,r;e.preventDefault(),"touchmove"===e.type?(t=e.touches[0].clientX-this.dragItems[this.dragCurrentItemIndex].initialX,r=e.touches[0].clientY-this.dragItems[this.dragCurrentItemIndex].initialY):(t=e.clientX-this.dragItems[this.dragCurrentItemIndex].initialX,r=e.clientY-this.dragItems[this.dragCurrentItemIndex].initialY),this.dragItemStyle="translate3d("+t+"px, "+r+"px, 0)",this.dragItems[this.dragCurrentItemIndex].currentX=t,this.dragItems[this.dragCurrentItemIndex].currentY=r,this.dragItems[this.dragCurrentItemIndex].offsetX=t,this.dragItems[this.dragCurrentItemIndex].offsetY=r,this.dragItems[this.dragCurrentItemIndex].style="translate3d("+t+"px, "+r+"px, 0)"}}},{kind:"method",key:"_handleAddElement",value:function(){const e={type:this.selectedElementType,entity:this.selectedEntityId,style:{position:"absolute",top:"50%",left:"50%",transform:""}};this.pictureElements.push(e);this.dragItems.push({currentX:0,currentY:0,initialX:0,initialY:0,offsetX:0,offsetY:0,style:""}),this.selectedEntityId="",this.selectedElementType="",this._handleCodeChanged()}},{kind:"method",key:"_handleSelectedElementTypeChanged",value:function(e){const t=e.detail.item.getAttribute("itemid");this.selectedElementType=t}},{kind:"method",key:"_handleSelectedEntityIdChanged",value:function(e){this.selectedEntityId=e.detail.value}},{kind:"method",key:"entityFilter",value:function(e){return!e.entity_id.includes(".ais")}},{kind:"method",key:"_handleCodeChanged",value:function(){this.codeValue="type: picture-elements\nimage: '/local/img/${this._params.title}'\ntitle: ''\nelements: [\n",this.pictureElements.forEach((e=>{this.codeValue+=JSON.stringify(e)+",\n"})),this.codeValue+="]"}},{kind:"method",key:"_addToLovelaceView",value:function(){var e;const t=null===(e=this._params)||void 0===e?void 0:e.sourceUrl.split("?authSig=")[0].replace("/media/galeria/"," /local/img/");(0,l.$)(this,this.hass,[],[{type:"picture-elements",title:"",image:t,elements:this.pictureElements}]),this.closeDialog()}},{kind:"method",key:"render",value:function(){return this._params&&this._params.sourceType&&this._params.sourceUrl?i.dy`
      <ha-dialog
        open
        hideActions
        .heading=${(0,a.i)(this.hass,"Konfiguracja karty elementy obrazu")}
        @closed=${this.closeDialog}
      >
        <div id="outerContainer">
          <div
            id="container"
            style="background-image: url(${this._params.sourceUrl});"
            @touchstart=${this._dragStart}
            @touchend=${this._dragEnd}
            @touchmove=${this._drag}
            @mousedown=${this._dragStart}
            @mouseup=${this._dragEnd}
            @mousemove=${this._drag}
          >
            ${this.pictureElements.map(((e,t)=>i.dy` <div
                .id=${t.toString()}
                class="pictureElementItem"
                .style=${this._getDragStyle(t)}
              >
                ${e.entity}
              </div>`))}
          </div>
        </div>
        <h3>Wybierz element do dodania</h3>
        <ha-paper-dropdown-menu dynamic-align label-float label="Typ">
          <paper-listbox
            slot="dropdown-content"
            attr-for-selected="itemId"
            .selected=${this.selectedElementType}
            @iron-select=${this._handleSelectedElementTypeChanged}
          >
            <paper-item itemid="state-badge">State Badge</paper-item>
            <paper-item itemid="state-icon">State Icon</paper-item>
            <paper-item itemid="state-label">State Label</paper-item>
          </paper-listbox>
        </ha-paper-dropdown-menu>
        <ha-entity-picker
          .hass=${this.hass}
          .value=${this.selectedEntityId}
          @value-changed=${this._handleSelectedEntityIdChanged}
          .configValue=${"entity"}
          .entityFilter=${this.entityFilter}
          allow-custom-entity
        ></ha-entity-picker>
        ${""!==this.selectedEntityId&&""!==this.selectedElementType?i.dy` <mwc-button @click=${this._handleAddElement}>
              <ha-svg-icon .path=${n.qX5}></ha-svg-icon>
              Dodaj element do obrazu
            </mwc-button>`:""}
        <br /><br />
        <ha-code-editor mode="yaml" .value=${this.codeValue}></ha-code-editor>
        <div class="card-actions">
          <mwc-button @click=${this._addToLovelaceView}>
            ${this.hass.localize("ui.panel.config.devices.entities.add_entities_lovelace")||"Dodaj do interfejsu użytkownika"}
          </mwc-button>
        </div>
      </ha-dialog>
    `:i.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[s.yu,i.iv`
        /* @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --mdc-dialog-min-width: 400px;
            width: 100%;
          }
        } */
        /* make dialog fullscreen */
        ha-dialog {
          --mdc-dialog-min-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          --mdc-dialog-max-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          --mdc-dialog-min-height: 100%;
          --mdc-dialog-max-height: 100%;
          --mdc-shape-medium: 0px;
          --vertial-align-dialog: flex-end;
        }
        #outerContainer {
          height: 50vh;
        }
        #container {
          height: 50vh;
          width: 50vw;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          border-radius: 7px;
          touch-action: none;
          background-size: 50vw 50vh;
          background-repeat: no-repeat;
          background-position: center;
          margin: auto;
        }
        div.pictureElementItem {
          width: 80px;
          height: 80px;
          background-color: rgb(245, 230, 99);
          border: 10px solid rgba(136, 136, 136, 0.5);
          border-radius: 50%;
          touch-action: none;
          user-select: none;
          top: 50%;
          left: 50%;
        }
        div.pictureElementItem:active {
          background-color: rgba(168, 218, 220, 1);
        }
        div.pictureElementItem:hover {
          cursor: pointer;
          /* border-width: 20px; */
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.b2a95715156189497a08.js.map