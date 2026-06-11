# MoMorph — FAQ・トラブルシューティングガイド

## ライセンス・運用

### <u>Essential と Pro の違い</u>

**❓ Q:** Essential と Pro のユーザープランはどのように異なりますか？

**💡 A:** ユーザーガイドによると、2 つのプランは機能の範囲が異なります。

- **Essential**: Plugin のみ利用できます — screen の管理、spec の手動入力、GitHub issue へのエクスポートが可能です。このプランでは Web App、Syncer、CLI、MCP、VSCode Extension、Claude Desktop Extension にはアクセスできません。
- **Pro**: エコシステム全体を利用できます — Plugin（フル機能）、Web、Syncer、CLI、MCP、VSCode Extension、Claude Desktop Extension。

Sun\* 社のドメインのメールアドレスを持つユーザーは、デフォルトで Pro アカウントになります。それ以外のメールアドレスの場合は、Pro アカウントの付与について MoMorph チームにお問い合わせください。

### <u>問い合わせ・サポート窓口</u>

**❓ Q:** MoMorph への質問やフィードバックは、どの窓口から送ればよいですか？

**💡 A:** 以下の窓口からお問い合わせいただけます。

- Slack: **#con_momorph-support_all**
- Email: **momorph-admin@sun-asterisk.com**

ご注意: 送信前に、プロジェクトの機密・秘密情報を含む画像は削除またはマスキングしてください。

## 不具合・障害

### <u>CLI で 'user not found' と表示される</u>

**❓ Q:** CLI で GitHub にログインした際に 'user not found' というメッセージが表示された場合はどうすればよいですか？

**💡 A:**

- `momorph login` で CLI に再ログインし、その後 `momorph whoami` で確認してください。
- あわせて、firewall／VPN が `github.com/login/device` をブロックしていないことを確認してください。

### <u>アカウントが GitHub プロジェクトに追加されていない</u>

**❓ Q:** GitHub に接続できず、アカウントがプロジェクトに追加されていないというメッセージが表示されます。どう対処すればよいですか？

**💡 A:** MoMorph Web 上で GitHub 連携を行ってください（Settings → GitHub → Connect repo）。

### <u>Item が表示されない、または順序が正しくない</u>

**❓ Q:** Figma のレイヤー名に番号を付けたのに、MoMorph で item が読み込まれない、または item の順序が正しくありません。どう対処すればよいですか？

**💡 A:** よくある原因は次のとおりです。

- レイヤー名の prefix `mms_` が正しくありません。Figma 上でレイヤー名を `mms_<名前>` の形式に変更してください。
- MoMorph 上のデータが Figma のレイヤーツリーの順序と同期しておらず、item の欠落や順序の誤りが生じています。

以下の方法で解消できます。

- MoMorph Plugin の Preview バーにある**更新（Refresh）**ボタンを押して、item を再読み込み・再同期してください。
- **「Find on Figma」**ボタンを使って、開いている item／screen が目的の Figma フレームと一致しているか確認してください。
- なお、非表示になっているレイヤーや最も外側の親フレームは読み込まれない点にご注意ください。

### <u>MoMorph 上の No の値が正しくない</u>

**❓ Q:** MoMorph 上の No の値が、Figma のレイヤー名に付けた prefix と一致しないのはなぜですか？

**💡 A:** これは MoMorph の設計上の動作です。

- Figma のレイヤー名に付けた番号は、MoMorph サーバーへの**初回のデータ同期時**にのみ Item No として使用されます。
- それ以降に「No」の値を変更したい場合は、MoMorph の「No」列で直接編集してください。システムは Figma へ逆同期しません。これにより、Web 上で編集した「No」の値が Figma のレイヤー名の番号と異なる場合のデータ不整合を防ぎます。

### <u>Figma フレーム差し替え後に spec が消える</u>

**❓ Q:** Figma でデザインを修正した後、MoMorph に入力した spec のデータが消えてしまいました。原因と対処方法を教えてください。

**💡 A:** この状況は、Figma の Paste to Replace 機能を使って元のフレームをより新しいデザインのフレームに差し替えた場合によく発生します。このとき、MoMorph 上の元のフレームは削除されます。元のフレームに対して作成した spec は保持されますが No UI（デザインなし）の状態に切り替わり、同時に新しいフレームが spec のない screen の一覧に表示されます。

原因は、Figma が差し替えたフレームに完全に新しい ID を割り当てるため、現時点では MoMorph が元のフレームを自動認識して spec データを新しいフレームへ移すことができないためです。

対処方法: MoMorph 上の元の screen（No UI 状態）の Preview エリアで、link frame 機能を使ってこの spec を新しいデザインフレームと紐付けてください。item の一覧では、UI Part 列も新しいフレームの対応するレイヤーと再度紐付ける必要があります。

### <u>AI 生成が途中で止まる</u>

**❓ Q:** AI によるコンテンツ生成が途中で止まったり、サーバーエラーが表示されたりした場合はどうすればよいですか？

**💡 A:**

- item が多い screen では、AI のコンテンツ生成に**30〜60 秒**ほどかかる場合があります。エラーと判断する前に、もう少しお待ちください。
- サーバーエラーが表示される場合は、MCP server が過負荷状態か、一時的な障害が発生している可能性があります。少し待ってから再度お試しください。

### <u>Google Sheets の同期エラー</u>

**❓ Q:** MoMorph と Google Sheets の間で spec を同期する際にエラーが発生した場合、どう対処すればよいですか？

**💡 A:** これは **MoMorph Syncer**（Google Add-on）の機能です。よくあるエラーは次のとおりです。

- **"Cannot access spreadsheet"**: ファイルは Sun\* 社の Google Workspace に属している必要があり、あなたのアカウントがそのファイルに対して **Editor** 権限を持っている必要があります（Viewer 権限では逆同期できません）。
- **"Missing authentication token"**: Google のログインセッションの有効期限が切れています。Sun\* 社のドメインのメールアドレスで再ログインし、Sheets のタブを再読み込みしてください。
- **"Failed to sync data"**: ネットワークまたはシステムの中断が原因の可能性があります。数分待ってから再度お試しください。

### <u>GitHub への spec エクスポート時のエラー</u>

**❓ Q:** spec を GitHub へ送る際にエラーが表示された場合、どう対処すればよいですか？

**💡 A:** GitHub 連携の設定画面を再度ご確認のうえ、GitHub アカウントとリポジトリの接続を一度切断し、再接続してみてください。

### <u>CSV ファイルの文字化け</u>

**❓ Q:** CSV ファイルを開いたときに文字化けする場合、何を確認すればよいですか？

**💡 A:** CSV ファイルを開くために使用しているツール（プレビューツール）を再度ご確認ください。ツールが正常に動作しているのに内容が引き続き正しく表示されない場合は、MoMorph チームにお問い合わせください。

## 設定・利用

### <u>AI 向けの Figma デザインのベストプラクティス</u>

**❓ Q:** デザイナーは AI と最も効果的に連携するために、Figma をどのように設計すればよいですか？

**💡 A:** 以下のヒントを参考にしてください。

- **構造・整理:** Pages を活用する。screen/item の名前を明確かつ一意に付ける（item 名の重複は、AI で item 一覧や spec を生成する際にエラーの原因となることがあります）。component を標準化する。不要な非表示のフレーム/レイヤーを削除する。screen が長くなりすぎないようにする。
- **設計テクニック:** Auto Layout を一貫して使う。edge case を含むすべての状態（states）を漏れなく設計する。Component Instance を規律をもって使用する。
- **Figma の構造:** 各 Frame は 1 つの screen に対応させる。Section の階層数は最大 7 階層程度に抑える（7 階層を超えると、MoMorph は 8 階層目以降の深い位置にある Frame を認識できない場合があります）。最初から階層構造を意識する。

### <u>item の命名規則（mms* / id*）</u>

**❓ Q:** MoMorph に認識させるための item の命名方法はどのようなもので、また旧形式の 'id\_' はいつサポートされなくなりますか？

**💡 A:**

- **新しい規則:** レイヤー名に prefix `mms_` を付けます。番号付けの内容は MoMorph 上で直接確認・編集できます。
- **旧規則:** prefix `id_` は 30/05/2026 以降は認識されなくなります。

### <u>spec 作成時のデータソース</u>

**❓ Q:** MoMorph は spec.md をデザインに基づいて作成しますか、それとも旧 spec に基づいて作成しますか？

**💡 A:** MoMorph は Figma 上のデザインから直接 spec を生成します。ただし、旧 spec も参照することで、変更点についてより詳細な分析を行うことができます。

### <u>Google Sheets の同期範囲</u>

**❓ Q:** Google Sheets で spec を編集した場合、その内容は Plugin/Web や spec.md（コード生成時に作成されるファイル）へ自動で更新されますか？

**💡 A:**

- Spreadsheet 上で変更した内容は、MoMorph Syncer の同期メニューを通じてのみ MoMorph サーバーに反映されます。
- この内容は spec.md ファイルへは自動で同期され**ません**。

### <u>AI に MoMorph から spec を取得させる</u>

**❓ Q:** Web 上での設定が完了した後、AI に MoMorph から spec を取得させるにはどうすればよいですか？

**💡 A:** 以下の手順で実施できます。

- CLI をインストールします: `brew install momorph/tap/momorph-cli`。
- `momorph login` を実行し、その後 `momorph init . --ai <agent>`（claude/copilot/cursor…）を実行して、MCP server と slash command を自動設定します。
- その後、AI agent が（slash command または通常のプロンプトを通じて）MCP tools を自動的に呼び出して spec を取得します — 例: `/downloadspecs` や screenId を含むプロンプトなど。

MCP を直接呼び出す必要はありません。

### <u>コード生成のワークフロー: MoMorph vs Takumi kit</u>

**❓ Q:** MoMorph と Takumi kit による AI でのコード生成の手順はどのように異なりますか？

**💡 A:**

- **MoMorph slash command（現行）:** `/specify` で spec.md、design-style.md、assets を生成することから始め、その後順に `/plan` → `/tasks` → `/implement` を実行します。これは MoMorph の公式ワークフローであり、引き続き完全にサポートされています。
- **Takumi kit（追加ツールキット）:** MoMorph をベースに統合されており、より柔軟です。`/create-plan` → `/takumi` を使うか、`/takumi` を直接呼び出します。利用するには Takumi kit を別途インストールする必要があります。

### <u>新しいバージョンが出たときの更新</u>

**❓ Q:** MoMorph の新しいバージョンが出ました。更新するには何をすればよいですか？

**💡 A:** Figma のキャッシュの仕組みにより、変更を反映するには次の順序どおりにリロードしてください: **1. Figma → 2. Plugin → 3. Web**。
