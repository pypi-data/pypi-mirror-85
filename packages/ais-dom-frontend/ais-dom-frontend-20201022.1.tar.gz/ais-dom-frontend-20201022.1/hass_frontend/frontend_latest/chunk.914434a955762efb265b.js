(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2747],{4268:(e,t,r)=>{"use strict";function i(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);t&&(i=i.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,i)}return r}function n(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){i(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function a(e,t){if(null==e)return{};var r,i,o=function(e,t){if(null==e)return{};var r,i,o={},n=Object.keys(e);for(i=0;i<n.length;i++)r=n[i],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);for(i=0;i<n.length;i++)r=n[i],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}function s(e,t){return!0===e?[]:!1===e?[t.fail()]:e}r.d(t,{DD:()=>l,Yj:()=>p,IX:()=>y,hu:()=>d,O7:()=>m,Rx:()=>b,Ry:()=>w,jt:()=>g,Z_:()=>k,n_:()=>_,dt:()=>E,G0:()=>O});class c{constructor(e){const{type:t,schema:r,coercer:i=(e=>e),validator:o=(()=>[]),refiner:n=(()=>[])}=e;this.type=t,this.schema=r,this.coercer=i,this.validator=o,this.refiner=n}}class l extends TypeError{constructor(e,t){const{path:r,value:i,type:o,branch:n}=e,s=a(e,["path","value","type","branch"]);super(`Expected a value of type \`${o}\`${r.length?` for \`${r.join(".")}\``:""} but received \`${JSON.stringify(i)}\`.`),this.value=i,Object.assign(this,s),this.type=o,this.path=r,this.branch=n,this.failures=function*(){yield e,yield*t},this.stack=(new Error).stack,this.__proto__=l.prototype}}function d(e,t){const r=h(e,t);if(r[0])throw r[0]}function u(e,t){const r=t.coercer(e);return d(r,t),r}function h(e,t,r=!1){r&&(e=t.coercer(e));const i=f(e,t),[o]=i;if(o){return[new l(o,i),void 0]}return[void 0,e]}function*f(e,t,r=[],i=[]){const{type:o}=t,a={value:e,type:o,branch:i,path:r,fail:(t={})=>n({value:e,type:o,path:r,branch:[...i,e]},t),check:(e,t,o,n)=>f(e,t,void 0!==o?[...r,n]:r,void 0!==o?[...i,o]:i)},c=s(t.validator(e,a),a),[l]=c;l?(yield l,yield*c):yield*s(t.refiner(e,a),a)}function p(){return _("any",(()=>!0))}function y(e){return new c({type:`Array<${e?e.type:"unknown"}>`,schema:e,coercer:t=>e&&Array.isArray(t)?t.map((t=>u(t,e))):t,*validator(t,r){if(Array.isArray(t)){if(e)for(const[i,o]of t.entries())yield*r.check(o,e,t,i)}else yield r.fail()}})}function m(){return _("boolean",(e=>"boolean"==typeof e))}function v(){return _("never",(()=>!1))}function b(){return _("number",(e=>"number"==typeof e&&!isNaN(e)))}function w(e){const t=e?Object.keys(e):[],r=v();return new c({type:e?`Object<{${t.join(",")}}>`:"Object",schema:e||null,coercer:e?j(e):e=>e,*validator(i,o){if("object"==typeof i&&null!=i){if(e){const n=new Set(Object.keys(i));for(const r of t){n.delete(r);const t=e[r],a=i[r];yield*o.check(a,t,i,r)}for(const e of n){const t=i[e];yield*o.check(t,r,i,e)}}}else yield o.fail()}})}function g(e){return new c({type:e.type+"?",schema:e.schema,validator:(t,r)=>void 0===t||r.check(t,e)})}function k(){return _("string",(e=>"string"==typeof e))}function _(e,t){return new c({type:e,validator:t,schema:null})}function E(e){const t=Object.keys(e);return _(`Type<{${t.join(",")}}>`,(function*(r,i){if("object"==typeof r&&null!=r)for(const o of t){const t=e[o],n=r[o];yield*i.check(n,t,r,o)}else yield i.fail()}))}function O(e){return _(""+e.map((e=>e.type)).join(" | "),(function*(t,r){for(const i of e){const[...e]=r.check(t,i);if(0===e.length)return}yield r.fail()}))}function j(e){const t=Object.keys(e);return r=>{if("object"!=typeof r||null==r)return r;const i={},o=new Set(Object.keys(r));for(const n of t){o.delete(n);const t=e[n],a=r[n];i[n]=u(a,t)}for(const e of o)i[e]=r[e];return i}}},95912:(e,t,r)=>{"use strict";r.r(t);r(53918),r(53268),r(12730);var i=r(50947),o=r(15652),n=r(81471),a=r(4268),s=r(87744),c=(r(31206),r(53822),r(16509),r(10983),r(26765)),l=(r(27849),r(11654));function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!f(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=m(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function u(e){var t,r=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const b=(0,a.dt)({title:(0,a.jt)((0,a.Z_)()),views:(0,a.IX)((0,a.Ry)())});!function(e,t,r,i){var o=d();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(p(n.descriptor)||p(o.descriptor)){if(f(n)||f(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(f(n)){if(f(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}h(n,o)}else t.push(n)}return t}(a.d.map(u)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("hui-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"closeEditor",value:void 0},{kind:"field",decorators:[(0,o.sz)()],key:"_saving",value:void 0},{kind:"field",decorators:[(0,o.sz)()],key:"_changed",value:void 0},{kind:"field",key:"_generation",value:()=>1},{kind:"method",key:"render",value:function(){return o.dy`
      <ha-app-layout>
        <app-header slot="header">
          <app-toolbar>
            <ha-icon-button
              icon="hass:close"
              @click="${this._closeEditor}"
            ></ha-icon-button>
            <div main-title>
              ${this.hass.localize("ui.panel.lovelace.editor.raw_editor.header")}
            </div>
            <div
              class="save-button
              ${(0,n.$)({saved:!1===this._saving||!0===this._changed})}"
            >
              ${this._changed?this.hass.localize("ui.panel.lovelace.editor.raw_editor.unsaved_changes"):this.hass.localize("ui.panel.lovelace.editor.raw_editor.saved")}
            </div>
            <mwc-button
              raised
              @click="${this._handleSave}"
              .disabled=${!this._changed}
              >${this.hass.localize("ui.panel.lovelace.editor.raw_editor.save")}</mwc-button
            >
          </app-toolbar>
        </app-header>
        <div class="content">
          <ha-code-editor
            mode="yaml"
            autofocus
            .rtl=${(0,s.HE)(this.hass)}
            .hass=${this.hass}
            @value-changed="${this._yamlChanged}"
            @editor-save="${this._handleSave}"
          >
          </ha-code-editor>
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"firstUpdated",value:function(){this.yamlEditor.value=(0,i.safeDump)(this.lovelace.config)}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,o.iv`
        :host {
          --code-mirror-height: 100%;
        }

        ha-app-layout {
          height: 100vh;
        }

        app-toolbar {
          background-color: var(--dark-background-color, #455a64);
          color: var(--dark-text-color);
        }

        mwc-button[disabled] {
          background-color: var(--mdc-theme-on-primary);
          border-radius: 4px;
        }

        .comments {
          font-size: 16px;
        }

        .content {
          height: calc(100vh - 68px);
        }

        hui-code-editor {
          height: 100%;
        }

        .save-button {
          opacity: 0;
          font-size: 14px;
          padding: 0px 10px;
        }

        .saved {
          opacity: 1;
        }
      `]}},{kind:"method",key:"_yamlChanged",value:function(){this._changed=!this.yamlEditor.codemirror.getDoc().isClean(this._generation),this._changed&&!window.onbeforeunload?window.onbeforeunload=()=>!0:!this._changed&&window.onbeforeunload&&(window.onbeforeunload=null)}},{kind:"method",key:"_closeEditor",value:async function(){this._changed&&!(await(0,c.g7)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_unsaved_changes"),dismissText:this.hass.localize("ui.common.no"),confirmText:this.hass.localize("ui.common.yes")}))||(window.onbeforeunload=null,this.closeEditor&&this.closeEditor())}},{kind:"method",key:"_removeConfig",value:async function(){try{await this.lovelace.deleteConfig()}catch(e){(0,c.Ys)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_remove","error",e)})}window.onbeforeunload=null,this.closeEditor&&this.closeEditor()}},{kind:"method",key:"_handleSave",value:async function(){this._saving=!0;const e=this.yamlEditor.value;if(!e)return void(0,c.g7)(this,{title:this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_remove_config_title"),text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_remove_config_text"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._removeConfig()});if(this.yamlEditor.hasComments&&!confirm(this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_unsaved_comments")))return;let t;try{t=(0,i.safeLoad)(e)}catch(r){return(0,c.Ys)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_parse_yaml","error",r)}),void(this._saving=!1)}try{(0,a.hu)(t,b)}catch(r){return void(0,c.Ys)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_invalid_config","error",r)})}t.resources&&(0,c.Ys)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.resources_moved")});try{await this.lovelace.saveConfig(t)}catch(r){(0,c.Ys)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_save_yaml","error",r)})}this._generation=this.yamlEditor.codemirror.getDoc().changeGeneration(!0),window.onbeforeunload=null,this._saving=!1,this._changed=!1}},{kind:"get",key:"yamlEditor",value:function(){return this.shadowRoot.querySelector("ha-code-editor")}}]}}),o.oi)}}]);
//# sourceMappingURL=chunk.914434a955762efb265b.js.map