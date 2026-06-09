# MoMorph — FAQ・トラブルシューティングガイド

> 出典: Slack `#con_momorph-support_all` のやり取り（2026年3月〜5月）＆ MoMorph ユーザーガイド（docs/user-guide）。最終更新: 2026/05/27。

## 不具合・障害

### Q1. Figma と MoMorph で番号が違って見えるのはなぜ？ (Plugin)

- Figma 上の番号は**最初の検出（detect）時のみ**使用されます。
- その後 MM 上で番号を変更する場合は、**MM の「No」列で直接編集**する必要があり、Figma からの逆同期はできません。

これは仕様であり、偶発的な不具合ではありません。

### Q2. 手動で番号を付けたのに一部の項目が表示・リンクされない？ (Plugin)

ユーザーガイドによると、よくある原因は **layer 名が `mms_` プレフィックス規則に従っていない**ことです（旧規則 `A_`・`1_` も可）。対処:

- Figma の layer 名を `mms_<名前>` 形式に修正（大文字小文字は区別しない）。
- Plugin の Preview ツールバーの **更新（Refresh）**ボタンで再読み込み。
- 非表示（visible=false）の layer や親 frame の opacity=0 は読み込まれません。

プレフィックスが正しいのに表示されない場合は不具合報告フォームへ（Q34 参照）。

### Q3. AI のコンテンツ生成が途中で止まり完了しない？ (AI生成)

AI 生成は **item の多い screen で 30〜60 秒かかる**ことがあります。エラーと判断する前に少し待ってください。それでも完了しない場合:

- `mcp.momorph.ai` へのネットワーク接続を確認。
- 再試行する（採番方法の変更も有効な場合あり）。
- 複数回失敗する場合は `momorph login` でトークンを更新。

繰り返す場合は不具合報告フォームへ（Q34 参照）。

### Q4. CSV ファイルが文字化けして表示される？ (Plugin)

CSV ファイルを開くプレビューツールを確認してください。プレビューツールに問題がないのに表示がおかしい場合は、Slack `#con_momorph-support_all` から MoMorph チームにお問い合わせください。

### Q5. 項目の番号が間違っている・順番が乱れている？ (Plugin)

多くは **MoMorph データと Figma ツリーの不整合**が原因です。対処:

- Figma で design を修正後、Preview ツールバーの **更新（Refresh）**ボタンで再同期。
- **「Find on Figma」**ボタンで item が正しい対象 frame を指しているか確認。

それでも誤る場合は MM チームに情報を提供して調査を依頼してください。

### Q6. Figma を更新したら MoMorph で入力したデータが消えた？ (Plugin)

Figma で design を修正・更新した後は、Plugin の Preview ツールバーの **更新（Refresh）**ボタンで再同期してください。それでも消える場合:

- 該当する **ScreenID** を MoMorph チームに提供。
- MM チームが影響を受けた screen のデータを再更新します。

### Q7. spec を GitHub に送るとエラーになる？ (サーバー)

複数のユーザーから報告されている問題です（日本語・ベトナム語の両方）。開発チームが対応中です。GitHub Issues 上の spec 表示の制約を解消するため、**「Github Flex」**という解決策が紹介されています。

### Q8. CLI で GitHub にログインすると「user not found」が出る？ (MCP・CLI)

- CLI に再ログイン: `momorph login` → `momorph whoami` で確認。
- firewall/VPN が `github.com/login/device` をブロックしていないか確認（同ページで code を直接入力も可）。
- **GitHub アカウント**接続と **repository** 接続の違いに注意（Q40 参照）。

### Q9. GitHub を連携できず、アカウントが未追加と表示される？ (Web)

CLI/MCP/VSCode を使うには **Pro ユーザー**が必要です:

- `@sun-asterisk.com` のメールは自動的に Pro。
- それ以外は Slack `#con_momorph-support_all` で Pro whitelist 追加を依頼。

また MoMorph Web で GitHub 連携が必要（file → Settings → GitHub → Connect repo）。

### Q10. AI 連携（MCP）がサーバーエラーで使えない？ (MCP・CLI)

MCP サーバーの過負荷または一時的なエラーが原因の可能性があります。しばらく待ってから再度お試しください。それでも復旧しない場合は、Slack `#con_momorph-support_all` からチームにご連絡ください。

### Q11. MoMorph と Google Sheets の spec 同期が失敗する？ (Web)

これは **MoMorph Syncer**（Google Add-on）の機能です。よくあるエラー:

- **「Cannot access spreadsheet」**: file が Sun* Workspace 内にあり、account が **Editor** 権限を持つ必要（Viewer は逆同期不可）。
- **「Missing authentication token」**: Google セッション切れ → `@sun-asterisk.com` で再ログインし Sheets タブを更新。
- **「Failed to sync data」**: backend/ネットワーク中断 → 数分待って再試行。

詳細なデバッグには Figma/Sheets の editor 権限を求める場合があります。

## 設定・接続

### Q12. Web 設定が完了。AI が spec を取得するには次に何をする？ (MCP・CLI)

手順:

- CLI をインストール: `brew install momorph/tap/momorph-cli`。
- `momorph login` → `momorph init . --ai <agent>`（claude/copilot/cursor…）で MCP server と slash command を自動設定。
- その後 AI agent が MCP tools を自動呼び出し（slash command または自然言語）して spec を取得 — 例 `/downloadspecs` や screenId 付きプロンプト。

ユーザーが MCP を直接呼ぶことはありません。

### Q13. GitHub 連携後もメンバーが Figma ファイルを開けない？ (Web)

- **admin** が GitHub を接続すると、repository のメンバーは Figma ファイルにアクセスできます。
- GitHub webhook がメンバー追加イベント（member-added event）の処理に失敗することがあります。
- **解決策:** GitHub を一時的に disconnect し、reconnect してください。

### Q14. Figma ファイルと GitHub リポジトリは何対何で連携できる？ (Web)

- 1 つの GitHub repository は複数の Figma ファイルに接続**できます**。
- 1 つの Figma ファイルを複数の repository に接続することは**できません**（逆方向は未対応、将来開発予定）。

### Q15. 顧客が MoMorph を使い始めるには何が必要？ (Web)

エコシステムをフル活用するには **Pro ユーザー**が必要です:

- `@sun-asterisk.com` は自動的に Pro。
- それ以外（顧客）は Slack `#con_momorph-support_all` で Pro whitelist 追加を依頼。

追加後、顧客にアカウント作成・ログインを案内してください。（Essential は Plugin のみ利用可。）

## リリース・採番

### Q16. MoMorph の新バージョン後、更新するには何をする？ (Plugin)

reload の順序（重要）: **1. Figma → 2. Plugin → 3. Web**。すでに plugin を開いている場合は、起動時に詳細画面（detail screen）を開いて同期（sync）することを推奨します。

### Q17. リリース履歴はどこで確認できる？ (サーバー)

リリース履歴の詳細は Slack `#con_momorph-support_all` の **Release Notes** を参照してください。**Figma Plugin** については MoMorph の Figma Community ページでバージョンを追跡できます: [figma.com/community/plugin/…/momorph](https://www.figma.com/community/plugin/1406117276934709483/momorph)。

### Q18. VSCode Extension v0.12.4 の新機能は？ (VSCode拡張)

- extension の起動（activation）メカニズムの改善。
- Figma Tree View 機能の追加。
- 検索・フィルター（search/filter）の改善。
- UI/UX の向上。

### Q19. 項目の命名ルールは？旧 'id_' はいつまで使える？ (Figma)

- **新ルール:** layer 名に prefix **mms_** を付与。採番内容は MoMorph 上で直接表示・編集できます。
- **旧ルール:** prefix **id_** — 2026/05/30 以降は認識されません。
- **自動マイグレーション期間:** 2026/03/27 〜 2026/05/29。

> ⚠️ 2026/05/29 以降、システムは id_ から mms_ への自動変換を行いません。期限までにマイグレーションを完了してください。

### Q20. 番号を変えたいとき、MoMorph と Figma どちらで直す？ (Plugin)

最初の detect 後に番号を変更したい場合は、Figma ではなく **MM の「No」列を編集**します。Figma 上の番号は最初の検出（initial detection）のためだけに使われます。

## 仕様・ワークフロー・Figma

### Q21. Google Sheets で spec を編集すると spec ファイルにも反映される？ (Web)

- Spreadsheet の内容は MoMorph DB にのみ保存されます。
- **spec.md ファイルへは自動同期されません。**
- BrSE が Spreadsheet で編集した情報は、処理の過程で AI が取り込み、markdown ファイルとして保存します。

### Q22. spec の「Note」と「Description」には何を書く？ (Web)

- **Description:** item の概要と、その item に対するユーザー操作（user interactions）を記述します。
- **Note:** spec 内の各 section の補足説明に使います。

button 型の item では、クリック時の DB 変更を「Description」に記載してください。

### Q23. MoMorph と Takumi kit の AI コード生成フローの違いは？ (MCP・CLI)

- **MoMorph slash commands（現行）:** `/specify` → spec.md + design-style.md + assets 生成 → `/plan` → `/tasks` → `/implement` の順に進む。MoMorph 公式ワークフローで、引き続きフルサポート。
- **Takumi kit（追加ツール）:** MoMorph の上に統合された補完ツール。`/create-plan` → `/takumi`、または直接 `/takumi` を実行。MoMorph slash command ではなく、Takumi kit の別途インストールが必要。

### Q24. AI と相性よく進めるため Designer は Figma をどう作る？ (Figma)

**構成・整理:** Pages を活用する; screen/item 名を正確で意味のあるものにする; component を標準化する; 不要な非表示 frame/layer を削除する; screen を長くしすぎない。

**設計技術:** Auto Layout を一貫して使う; edge case を含むすべての states を設計する; Component Instance を規律をもって使う。

**Figma 構造:** 1 Frame = 1 画面; Section の入れ子（nesting）には制限がある; 設計初期から階層構造を意識する。

### Q25. Figma で項目名が重複するとどうなる？ (Figma)

item 名の重複は MoMorph 上でエラーを引き起こす可能性があります。報告済みで、チームが対策を検討中です。ベストプラクティス: 同一スコープ内で **常に item 名を一意にする**こと。

### Q26. MoMorph は spec をデザインから作る？既存 spec を参照する？ (AI生成)

MoMorph チームの説明: MM は **Figma design から直接、妥当な spec を生成**します。既存の spec.md を参照しなくても生成可能ですが、参照しない場合は詳細な分析が難しくなります。設計上の目的は design 自体から妥当な spec を作ることです。(spec 同期は Q21 参照)

### Q27. MoMorph 向け Figma 設計で気をつける制限は？ (Figma)

- **Frame = 1 画面:** MoMorph は各 Frame を独立した screen として読み取ります。
- **Section の入れ子制限:** 深さ（nesting）に制限があり、深くしすぎないこと。
- 推奨（必須ではない）: 不要な layer を作らない。
- 設計開始時から階層構造を意識すること。

Figma 有料プランの契約は、デザイン変更の頻度に応じて判断すべきで、チーム全員が契約する必要はありません。

## ライセンス・運用

### Q28. プロジェクト情報を共通サポートチャンネルに投稿してよい？ (共通)

プロジェクト情報漏洩を防ぐため: 共通チャンネルでは PJ 情報を含む内容の投稿を控える; 詳細なやり取りが必要な場合は専用の DM グループを使う（必要に応じて MoMorph チームの担当者を追加）。

### Q29. Essential と Pro プランの違いは？ (ライセンス)

ユーザーガイドより:

- **Essential**: **Plugin のみ** — screen 管理、spec 手動入力、GitHub issue export。Web App・Syncer・CLI・MCP・VSCode Extension・Claude Desktop Extension は利用不可。
- **Pro**: **エコシステム全体** — Plugin（フル）+ Web + Syncer + CLI + MCP + VSCode Extension + Claude Desktop Extension。

`@sun-asterisk.com` は自動 Pro。それ以外は Slack で whitelist 追加を依頼。

### Q30. MoMorph の AI（Copilot・Claude Code）の利用と料金は？ (ライセンス)

- spec・test case 生成: MoMorph BE または Copilot を利用可能。
- コード生成: Claude Code を推奨。フェーズに応じて Claude Code Premium Seat を申請可能。
- Copilot にはライセンスプランごとの利用制限があります。

### Q31. AI（MCP）利用時に認証エラー、よくある原因は？ (MCP・CLI)

多くは **GitHub PAT の revoke/期限切れ**です（`x-github-token invalid / 401` エラー）。対処:

- scope `user` の新しい PAT を作成し MCP config（例 `~/.claude.json`）を更新。
- `momorph init` 利用時は `momorph login` でトークンが自動マージされます。

### Q32. MoMorph への質問・フィードバックはどのチャンネル？ (共通)

フィードバック受付チャンネルは **#con_momorph-support_all** に統合されました。旧チャンネル #temp_archived_moved-to-con_mormorph-support_all は archive 済みです。

### Q33. MoMorph の利用マニュアルはある？ (共通)

あります。MoMorph チームが公式資料を提供しています:

- **MoMorph — ユーザーガイド**（Plugin・Web・Syncer・CLI・MCP・VSCode Extension・Claude Desktop Extension）— EN/JP/VI 版。
- **MoMorph MCP Server — Tools Reference**（31 tools の詳細）。
- Release Notes・Testplay・Q&A List。

ファイルは Slack `#con_momorph-support_all` で直接依頼してください。

### Q34. 不具合に遭遇したとき、どう報告すればよい？ (共通)

上記いずれかの不具合に遭遇した場合:

- MoMorph チームの要請に従い、**詳細な不具合報告フォーム**を記入する。
- 送信前に、**機密・秘密情報を含む画像を削除またはマスク**する。

特定の screen データに関係する場合は、ScreenID を提供すると対応が速くなります。

## 機能要望

### Q35. spec に概要説明の欄を追加できる？ (Web)

正式な要望: AIDD のプロセスでは概要を記述する「overview description」フィールドが必要ですが、現在 MoMorph では未提供です。この要望は MoMorph チームへ送付済みです。

### Q36. List Item に複数行をまとめて貼り付けできる？ (Web)

現在、List Item への複数行入力は不便です。外部ソース（Excel、テキスト）から List Item へ複数行をコピー＆ペーストする機能の要望があります。

### Q37. 項目名が重複したとき MoMorph 側で対応してくれる？ (Figma)

item 名の重複によるエラーについて、MoMorph チームに解決策の検討を要望しています。現状は「一意の名前を付ける」という推奨のみで、重複時に MoMorph 側がより柔軟に処理することが望まれています。

### Q38. MoMorph への機能要望はどこから送る？ (共通)

機能要望を送るための公式フォーム/チャンネルがあるか質問が出ています — 構造化された機能要望の受付の仕組みが望まれています。

### Q39. MoMorph は新機能リリース前に意見を聞いてくれる？ (共通)

要望: 新機能リリース前にフィードバックを収集する仕組みと、ユーザーが準備できるよう release notes の事前通知（advance notification）が望まれています。

### Q40. GitHub アカウントとリポジトリ接続が紛らわしい、改善予定は？ (Web)

多くのユーザーが「GitHub アカウントの接続」と「repository の接続」を混同しています。2 つの概念が明確に区別され、誤解を生まないよう UI の改善が提案されています。

### Q41. Excel 同期時、MoMorph にない列は失われる？ (Web)

現在、MM に存在しない field は Excel に手入力する必要があります。MoMorph が表示 field をフィルタリングせず、MM が未管理の field も含めすべての field を保持/表示できるようにし、手入力の手間を減らす要望です。

---

## 重要な日程

- 2026/03/27: id_ → mms_ への自動マイグレーション開始
- 2026/05/29: id_ → mms_ 自動マイグレーション期間の終了
- 2026/05/30: システムが id_ プレフィックスの認識を停止

## 主な問い合わせ先

| 役割 | 担当者 |
| --- | --- |
| PM / リリースマネージャー | 種井彩誉, 古川優人, Thanh, nguyen.hien |
| テックリード / エンジニアリング | le.minh.hoang |
| プロジェクト課題サポート | Thanh, tran.quoc.luc |

主なサポートチャンネル: **#con_momorph-support_all**
