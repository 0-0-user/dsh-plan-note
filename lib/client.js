window.__ModuleLoader__.load({
	id: "dsh-plan-note",
	factory: (require) => {
		var module = { exports: {} };
		var exports = module.exports;
		var React = require("react");
		var primitives = require("@deepseek-ai/dsh-client-ui-primitives");
		var h = React.createElement;
		var MarkdownText = primitives.MarkdownText;

		var inject = ["slots", "sidebarRight", "sidebarRightTabs"];
		var TAB_KIND = "plan-note";
		var TAB_ID = "plan-note";
		var HIGHLIGHT_NAME = "plan-note-mark";
		var HIGHLIGHT_STYLE_ID = "dsh-plan-note-style";

		// Shared review state, read by both the composer bar and the sidebar pane.
		var state = {
			questionId: null,
			plan: "",
			approveLabel: "同意执行",
			declineLabel: "要求修改",
			comments: [],
			note: "",
			selection: null,
			draft: "",
			error: null,
			busy: false
		};
		var listeners = new Set();
		var nextCommentId = 1;
		var closePane = null;

		function emit() {
			listeners.forEach(function (listener) {
				listener();
			});
		}

		function patch(changes) {
			state = Object.assign({}, state, changes);
			emit();
		}

		function subscribe(listener) {
			listeners.add(listener);
			return function () {
				listeners.delete(listener);
			};
		}

		function useStore() {
			return React.useSyncExternalStore(subscribe, function () {
				return state;
			});
		}

		function planReviewOf(pending) {
			if (pending === null || typeof pending !== "object") return null;
			var questions = pending.questions;
			if (!Array.isArray(questions) || questions.length !== 1) return null;
			var question = questions[0];
			if (question === null || typeof question !== "object") return null;
			var intent = question.intent;
			if (intent === null || typeof intent !== "object") return null;
			if (intent.kind !== "plan-review") return null;
			if (typeof question.detail !== "string" || question.detail === "") return null;
			return question;
		}

		function truncate(text, max) {
			var value = String(text).replace(/\s+/g, " ").trim();
			return value.length > max ? value.slice(0, max) + "…" : value;
		}

		function resetFor(question) {
			var approve = question && question.intent && typeof question.intent.approve === "string"
				? question.intent.approve
				: "同意执行";
			var decline = "要求修改";
			if (question && Array.isArray(question.options)) {
				var other = question.options.find(function (option) {
					return option && option.label && option.label !== approve;
				});
				if (other) decline = other.label;
			}
			state = {
				questionId: question ? question.id : null,
				plan: question ? question.detail : "",
				approveLabel: approve,
				declineLabel: decline,
				comments: [],
				note: "",
				selection: null,
				draft: "",
				error: null,
				busy: false
			};
			try {
				var raw = window.sessionStorage.getItem("dsh-plan-note:" + (question ? question.id : "unknown"));
				if (raw) {
					var saved = JSON.parse(raw);
					if (saved && Array.isArray(saved.comments)) state.comments = saved.comments;
					if (saved && typeof saved.note === "string") state.note = saved.note;
					state.comments.forEach(function (comment) {
						var numeric = parseInt(String(comment.id).replace(/^c/, ""), 10);
						if (!isNaN(numeric) && numeric >= nextCommentId) nextCommentId = numeric + 1;
					});
				}
			} catch (e) {
				/* ignore corrupt drafts */
			}
			emit();
		}

		function persist() {
			try {
				window.sessionStorage.setItem("dsh-plan-note:" + (state.questionId || "unknown"), JSON.stringify({
					comments: state.comments,
					note: state.note
				}));
			} catch (e) {
				/* storage may be unavailable */
			}
		}

		function composeFeedback() {
			var parts = [];
			if (state.comments.length > 0) {
				parts.push("## 计划批注（" + state.comments.length + " 条）");
				state.comments.forEach(function (comment, index) {
					parts.push("");
					parts.push((index + 1) + ". 原文：「" + comment.quote.replace(/\s+/g, " ").trim() + "」");
					parts.push("   意见：" + comment.note.replace(/\s+/g, " ").trim());
				});
			}
			if (state.note.trim() !== "") {
				parts.push("");
				parts.push("## 整体意见");
				parts.push(state.note.trim());
			}
			return parts.join("\n");
		}

		// ------------------------------------------------------------------
		// Text-range helpers for the CSS Custom Highlight API.
		// ------------------------------------------------------------------

		function collectTextNodes(root) {
			var nodes = [];
			var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
			var node = walker.nextNode();
			while (node) {
				nodes.push(node);
				node = walker.nextNode();
			}
			return nodes;
		}

		function findRange(root, quote, occurrence) {
			if (quote === "") return null;
			var nodes = collectTextNodes(root);
			var full = nodes.map(function (node) { return node.nodeValue; }).join("");
			var index = -1;
			var from = 0;
			for (var i = 0; i <= occurrence; i += 1) {
				index = full.indexOf(quote, from);
				if (index < 0) return null;
				from = index + quote.length;
			}
			var startNode = null;
			var startOffset = 0;
			var endNode = null;
			var endOffset = 0;
			var cursor = 0;
			for (var n = 0; n < nodes.length; n += 1) {
				var length = nodes[n].nodeValue.length;
				if (startNode === null && index < cursor + length) {
					startNode = nodes[n];
					startOffset = index - cursor;
				}
				if (startNode !== null && index + quote.length <= cursor + length) {
					endNode = nodes[n];
					endOffset = index + quote.length - cursor;
					break;
				}
				cursor += length;
			}
			if (startNode === null || endNode === null) return null;
			var range = document.createRange();
			range.setStart(startNode, startOffset);
			range.setEnd(endNode, endOffset);
			return range;
		}

		function ensureHighlightStyle() {
			if (document.getElementById(HIGHLIGHT_STYLE_ID)) return;
			var style = document.createElement("style");
			style.id = HIGHLIGHT_STYLE_ID;
			style.textContent = "::highlight(" + HIGHLIGHT_NAME + "){text-decoration:underline;text-decoration-color:#d33;text-decoration-thickness:2px;text-underline-offset:2px;}";
			document.head.appendChild(style);
		}

		function applyHighlights(root) {
			if (typeof CSS === "undefined" || !CSS.highlights || typeof Highlight === "undefined") return;
			ensureHighlightStyle();
			var ranges = [];
			state.comments.forEach(function (comment) {
				var range = findRange(root, comment.quote, comment.occurrence || 0);
				if (range) ranges.push(range);
			});
			if (ranges.length === 0) {
				CSS.highlights.delete(HIGHLIGHT_NAME);
				return;
			}
			CSS.highlights.set(HIGHLIGHT_NAME, new Highlight(...ranges));
		}

		// ------------------------------------------------------------------
		// Styling: inherit the host palette; one button shape everywhere.
		// ------------------------------------------------------------------

		var BORDER = "1px solid rgba(127,127,127,0.35)";
		var SOFT_BG = "rgba(127,127,127,0.06)";
		var MUTED = "rgba(127,127,127,0.85)";

		var MARKDOWN_LABELS = {
			code: {
				copyLabel: "复制",
				copiedLabel: "已复制",
				toolbarLabels: {
					codeLabel: "代码",
					wrapLabel: "换行",
					unwrapLabel: "不换行"
				}
			},
			footnotes: "脚注"
		};

		var MarkdownBoundary = class MarkdownBoundary extends React.Component {
			constructor(props) {
				super(props);
				this.state = { failed: false };
			}
			static getDerivedStateFromError() {
				return { failed: true };
			}
			render() {
				if (this.state.failed) {
					return React.createElement("pre", {
						style: { whiteSpace: "pre-wrap", font: "inherit", margin: 0 }
					}, this.props.fallbackText);
				}
				return this.props.children;
			}
		};


		function buttonStyle(disabled) {
			return {
				padding: "5px 12px",
				borderRadius: "6px",
				border: disabled ? "1px solid transparent" : BORDER,
				background: "transparent",
				color: disabled ? "rgba(127,127,127,0.45)" : "inherit",
				cursor: disabled ? "default" : "pointer",
				font: "inherit",
				fontSize: "12.5px",
				lineHeight: "1.2"
			};
		}

		var S = {
			pane: {
				display: "flex",
				flexDirection: "column",
				height: "100%",
				minHeight: "0",
				color: "inherit",
				font: "inherit"
			},
			planScroll: {
				flex: "1 1 0",
				overflow: "auto",
				padding: "12px 16px",
				minHeight: "120px"
			},
			section: {
				borderTop: BORDER,
				padding: "10px 16px",
				background: SOFT_BG
			},
			commentsSection: {
				borderTop: BORDER,
				padding: "10px 16px",
				background: SOFT_BG,
				flex: "0 1 auto",
				maxHeight: "30vh",
				overflow: "auto"
			},
			noteSection: {
				borderTop: BORDER,
				padding: "10px 16px",
				background: SOFT_BG,
				flex: "0 0 auto"
			},
			item: {
				border: BORDER,
				borderRadius: "6px",
				padding: "5px 8px",
				marginBottom: "5px",
				fontSize: "12px",
				lineHeight: "1.55"
			},
			quote: {
				color: MUTED,
				fontSize: "11.5px",
				borderLeft: "2px solid rgba(127,127,127,0.4)",
				paddingLeft: "8px",
				marginBottom: "2px",
				whiteSpace: "pre-wrap"
			},
			textarea: {
				width: "100%",
				minHeight: "52px",
				resize: "vertical",
				border: BORDER,
				borderRadius: "6px",
				background: "transparent",
				color: "inherit",
				padding: "6px 8px",
				font: "inherit",
				fontSize: "12.5px",
				boxSizing: "border-box"
			},
			bar: {
				display: "flex",
				alignItems: "center",
				gap: "8px",
				padding: "8px 12px",
				border: BORDER,
				borderRadius: "8px",
				background: SOFT_BG,
				color: "inherit",
				font: "inherit",
				fontSize: "13px"
			}
		};

		// ------------------------------------------------------------------
		// Sidebar pane.
		// ------------------------------------------------------------------

		function PlanNotePane(props) {
			var snapshot = useStore();
			var planRef = React.useRef(null);
			var info = props && typeof props.useTabInfo === "function" ? props.useTabInfo() : null;

			React.useEffect(function () {
				closePane = function () {
					try {
						if (info && info.tab && info.tab.actions && typeof info.tab.actions.close === "function") {
							info.tab.actions.close();
						}
					} catch (e) {
						/* leave the tab open */
					}
				};
				return function () {
					closePane = null;
				};
			}, []);

			React.useEffect(function () {
				if (planRef.current) applyHighlights(planRef.current);
			}, [snapshot.comments, snapshot.plan]);

			function onMouseUp() {
				var container = planRef.current;
				var selection = window.getSelection();
				if (!container || !selection || selection.isCollapsed || selection.rangeCount === 0) return;
				var range = selection.getRangeAt(0);
				if (!container.contains(range.startContainer) || !container.contains(range.endContainer)) return;
				var quote = selection.toString();
				if (quote.trim() === "") return;
				var same = snapshot.comments.filter(function (comment) {
					return comment.quote === quote;
				}).length;
				patch({ selection: { quote: quote, occurrence: same }, draft: "", error: null });
			}

			function addComment() {
				if (!snapshot.selection) return;
				var body = snapshot.draft.trim();
				if (body === "") {
					patch({ error: "先写一句意见，再添加批注" });
					return;
				}
				var comment = {
					id: "c" + String(nextCommentId++),
					quote: snapshot.selection.quote,
					occurrence: snapshot.selection.occurrence,
					note: body
				};
				patch({ comments: snapshot.comments.concat([comment]), selection: null, draft: "", error: null });
				persist();
				try {
					window.getSelection().removeAllRanges();
				} catch (e) {
					/* ignore */
				}
			}

			function locate(comment) {
				var container = planRef.current;
				if (!container) return;
				var range = findRange(container, comment.quote, comment.occurrence || 0);
				if (!range) return;
				var rect = range.getBoundingClientRect();
				container.scrollTop += rect.top - container.getBoundingClientRect().top - 60;
			}

			var list = snapshot.comments.length === 0
				? h("div", { style: { color: MUTED, fontSize: "12px" } }, "在计划里选中文字，就能加批注。")
				: h("div", null, snapshot.comments.map(function (comment, index) {
					return h("div", { key: comment.id, style: S.item },
						h("div", { style: S.quote }, "「" + truncate(comment.quote, 140) + "」"),
						h("div", { style: { whiteSpace: "pre-wrap" } }, (index + 1) + ". " + comment.note),
						h("div", { style: { display: "flex", gap: "4px" } },
							h("button", { style: buttonStyle(false), onClick: function () { locate(comment); } }, "定位"),
							h("button", {
								style: buttonStyle(false),
								onClick: function () {
									patch({
										comments: snapshot.comments.filter(function (item) {
											return item.id !== comment.id;
										})
									});
									persist();
								}
							}, "删除")
						)
					);
				}));

			return h("div", { style: S.pane },
				h("div", { style: { padding: "6px 16px", borderBottom: BORDER, fontSize: "12px", color: MUTED } },
					"计划正文 · 批注 " + snapshot.comments.length + " 条"),
				h("div", { style: S.planScroll, ref: planRef, onMouseUp: onMouseUp },
					h(MarkdownBoundary, { fallbackText: snapshot.plan },
						h(MarkdownText, { text: snapshot.plan, labels: MARKDOWN_LABELS })
					)
				),
				h("div", { style: S.commentsSection },
					h("div", { style: { fontWeight: 600, marginBottom: "6px" } },
						"批注 " + snapshot.comments.length + " 条",
						snapshot.error ? h("span", { style: { color: "#c0392b", fontWeight: 400, marginLeft: "8px" } }, snapshot.error) : null
					),
					list,
					snapshot.selection
						? h("div", { style: { display: "flex", flexDirection: "column", gap: "6px", marginTop: "6px" } },
							h("div", { style: { color: MUTED, fontSize: "12px" } }, "已选：" + truncate(snapshot.selection.quote, 60)),
							h("textarea", {
								style: S.textarea,
								placeholder: "针对这段原文写意见",
								value: snapshot.draft,
								onChange: function (event) {
									patch({ draft: event.target.value });
								}
							}),
							h("div", { style: { display: "flex", gap: "6px" } },
								h("button", { style: buttonStyle(false), onClick: addComment }, "添加批注"),
								h("button", {
									style: buttonStyle(false),
									onClick: function () {
										patch({ selection: null, draft: "" });
									}
								}, "取消")
							)
						)
						: null
				),
				h("div", { style: S.noteSection },
					h("div", { style: { color: MUTED, fontSize: "12px", marginBottom: "6px" } }, "整体意见（可留空）"),
					h("textarea", {
						style: S.textarea,
						value: snapshot.note,
						onChange: function (event) {
							patch({ note: event.target.value });
							persist();
						}
					})
				)
			);
		}

		// ------------------------------------------------------------------
		// Composer bar.
		// ------------------------------------------------------------------

		function PlanNoteBar(props) {
			var ctx = props.ctx;
			var pending = props.pending;
			var question = props.question;
			var snapshot = useStore();
			var fallbackState = React.useState(false);
			var fallback = fallbackState[0];
			var setFallback = fallbackState[1];

			React.useEffect(function () {
				resetFor(question);
				try {
					ctx.sidebarRight.openTab(TAB_KIND);
				} catch (error) {
					setFallback(true);
				}
			}, []);

			var hasComments = snapshot.comments.length > 0;

			function settle(send) {
				patch({ busy: true, error: null });
				send().then(function () {
					try {
						window.sessionStorage.removeItem("dsh-plan-note:" + (state.questionId || "unknown"));
					} catch (e) {
						/* ignore */
					}
					if (typeof closePane === "function") closePane();
				}).catch(function (cause) {
					patch({ busy: false, error: cause instanceof Error ? cause.message : String(cause) });
				});
			}

			function sendFeedback() {
				if (snapshot.busy) return;
				var text = composeFeedback();
				if (text === "") {
					patch({ error: "还没有写批注或整体意见" });
					return;
				}
				settle(function () {
					return pending.answer({
						answers: [{ id: question.id, selected: [state.declineLabel], custom: text }]
					});
				});
			}

			function approve() {
				if (snapshot.busy || hasComments) return;
				settle(function () {
					return pending.answer({ answers: [{ id: question.id, selected: [state.approveLabel] }] });
				});
			}

			var disabledByComments = hasComments || snapshot.busy;

			return h("div", null,
				h("div", { style: S.bar },
					h("span", { style: { fontWeight: 600 } }, "计划批注"),
					h("span", { style: { color: MUTED } }, snapshot.comments.length + " 条"),
					snapshot.error ? h("span", { style: { color: "#c0392b" } }, snapshot.error) : null,
					h("span", { style: { flex: "1 1 auto" } }),
					h("button", { style: buttonStyle(false), onClick: sendFeedback, disabled: snapshot.busy }, "发送批注"),
					h("button", { style: buttonStyle(disabledByComments), onClick: approve, disabled: disabledByComments }, "同意执行"),
					h("button", {
						style: buttonStyle(disabledByComments),
						disabled: disabledByComments,
						onClick: function () {
							if (!disabledByComments) pending.dismiss();
						}
					}, "关闭")
				),
				fallback ? h("div", { style: { marginTop: "8px", border: BORDER, borderRadius: "8px", maxHeight: "52vh", overflow: "auto" } }, h(PlanNotePane)) : null
			);
		}

		function PlanNoteComposer(props) {
			var pending = props.matched;
			var question = planReviewOf(pending);
			if (!question) return null;
			return h(PlanNoteBar, { ctx: props.ctx, pending: pending, question: question });
		}

		// ------------------------------------------------------------------
		// Plugin entry.
		// ------------------------------------------------------------------

		function apply(ctx) {
			ctx.effect(function () {
				return ctx.sidebarRightTabs.register({
					id: TAB_ID,
					kind: TAB_KIND,
					title: function () {
						return "计划批注";
					}
				});
			}, "plan-note: sidebar tab type");

			ctx.effect(function () {
				return ctx.slots.register({
					name: "sidebar.right.pane.tab",
					key: TAB_ID,
					inject: function () {
						return {};
					}
				}, PlanNotePane);
			}, "plan-note: sidebar pane body");

			ctx.slots.inject("conversation.composer", function () {
				return ctx.slots.register({
					name: "conversation.composer",
					select: function (props) {
						return planReviewOf(props.pendingInteraction) ? props.pendingInteraction : null;
					},
					inject: function () {
						return { ctx: ctx };
					}
				}, PlanNoteComposer);
			});
		}

		exports.apply = apply;
		exports.inject = inject;
		return module.exports;
	}
});
