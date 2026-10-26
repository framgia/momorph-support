# V1からV2への移行

![新MoMorphの公開告知（2026年11月4日）](images/v2/momorph-2-launch-banner.webp)

新MoMorph（V2）は、2026年11月4日に公開します。旧MoMorph（V1）は、11月30日に提供を終了します。このページでは、旧MoMorphから変わる点、移行されるデータ、利用中の方へのお願いを説明します。新MoMorphの使い方は、[MoMorph V2の使い方](v2-user-guide.md)を参照してください。

## 1. 移行スケジュール {#schedule}

```mermaid
flowchart LR
  A["〜11/1（日）<br>下書きの画面仕様を<br>旧MoMorphに保存"] --> B["11/2（月）〜3（火）<br>新旧とも操作不可"] --> C["11/4（水）<br>新MoMorphを公開<br>旧MoMorphは閲覧のみ"] --> D["11/30（月）<br>旧MoMorphの提供終了"]
```

| 日付 | 内容 | 利用者の対応 |
|---|---|---|
| 〜11/1（日） | 旧MoMorphで作業できる最終日 | 下書きの画面仕様を、旧MoMorphに**保存**する |
| 11/2（月）〜3（火） | データの移行 | **新旧とも操作できない** |
| 11/4（水） | 新MoMorphを公開。旧MoMorphは閲覧のみ | 新MoMorphにログインし、データを確認する |
| 11/30（月） | 旧MoMorphの提供終了 | 必要な情報を、この日までに確認する |

!!! warning "11/1（日）までに保存してください"
    保存していない下書きの画面仕様は、新MoMorphに移行されません。

## 2. 旧MoMorphから変わる主な点 {#changes}

| 変わる点 | 旧MoMorph | 新MoMorph |
|---|---|---|
| ログイン | Figmaのアカウント | GoogleまたはGitHubのアカウント |
| 使える人 | プラン（Essential、Pro）による | 管理者の招待、または参加申請の承認 |
| AIでの仕様作成 | 製品内の生成ボタン | 生成ボタンを廃止。Claude CodeなどのAIから依頼 |
| 議論とレビュー | 画面へのコメント | キャンバスのコメントと承認スタンプ |
| 画面タグ | タグで絞り込み | 廃止。ステータスとFigmaページで絞り込む |
| エクスポート | 複数の形式 | CSVに一本化 |
| Web | `momorph.ai` | `app.momorph.ai` |

## 3. 移行されるデータ {#migrated-data}

主な仕様データは、新MoMorphに引き継がれます。

```mermaid
flowchart LR
  subgraph 旧MoMorph
    F1["仕様を入力した<br>Figmaファイル"] --> S1["画面<br>Figmaで削除済みでも、<br>仕様を入力した画面を含む"]
    S1 --> I1["画面の仕様、進捗状況"]
    U1["メンバー"]
  end
  subgraph 新MoMorph
    P2["プロジェクト"] --> S2["画面"] --> I2["仕様、進捗ステータス"]
    M2["メンバー"]
  end
  F1 --> P2
  S1 --> S2
  I1 --> I2
  U1 --> M2
```

| 移行される | 移行されない |
|---|---|
| 仕様を入力したFigmaファイル | 仕様のないFigmaファイル |
| そのファイルの画面、画面の仕様、進捗状況、メンバー | 削除、アーカイブした画面 |
| Figmaで削除済みでも、仕様を入力した画面 | プレビュー画像 |

### 移行されないデータの扱い {#not-migrated}

| 区分 | データ | 扱い |
|---|---|---|
| プレビュー画像 | 画面のプレビュー画像 | MoMorph Figma Pluginを開くと再保存される |
| 未開発の機能 | 仕様の履歴、スプレッドシート出力、GitHub課題登録 | 12月に開発を予定 |
| 提供を終える機能 | 画面の翻訳、画面へのコメント、画面のグループ、画面のテストケース、登録したプロンプト、アップロードした辞書、操作履歴、画面タグ | 移行しない |

## 4. 利用者が行う作業 {#user-steps}

```mermaid
flowchart LR
  A["1. 11/1までに<br>下書きを保存"] --> B["2. 11/4以降、旧と同じ<br>メールアドレスでログイン"] --> C["3. 移行された<br>データを確認"] --> D["4. momoneoを<br>インストールし、<br>AIを接続し直す"]
```

### 4.1 旧MoMorphと同じメールアドレスでログインする {#login-same-email}

旧MoMorphと**同じメールアドレス**でログインすると、移行したデータが表示されます。

```mermaid
flowchart TD
  L["新MoMorphにログイン"] --> Q{"旧MoMorphと同じ<br>メールアドレス？"}
  Q -- "同じ" --> OK["移行したデータが表示される"]
  Q -- "違う" --> NG["移行したデータは表示されない"]
  NG --> R["ログアウトし、旧MoMorphの<br>メールアドレスで再ログイン"]
```

### 4.2 移行されたデータを確認する {#check-data}

1. **「プロジェクト一覧」**で、旧MoMorphのFigmaファイルにあたるプロジェクトを開きます。
2. 画面一覧、画面の仕様、進捗ステータスを確認します。

### 4.3 プラグインとAIの接続をやり直す {#reconnect}

旧MoMorphのプラグインとMCP設定は、新MoMorphでは使えません。次の手順で設定し直します。

- プラグイン「momoneo」：[1.7 Figma Pluginにログイン](v2-user-guide.md#login-plugin)
- APIキーとAIの接続：[1.5 APIキーの発行](v2-user-guide.md#api-key)、[1.6 MCPでAIアシスタントと接続](v2-user-guide.md#connect-ai)

## 5. 旧MoMorphのドキュメント {#v1-docs}

旧MoMorphのドキュメントは、**アーカイブ（V1）**にあります。

- [V1 総合ユーザーガイド](archived/general-user-guide.md)
- [V1 MCPツールリファレンス](archived/mcp-tools-reference.md)
- [V1 よくある質問](archived/faq.md)
- [V1 リリースノート](archived/release-notes.md)

## 6. お問い合わせ {#contact}

Slackの`#con_momorph-support_all`にあるフォームから送信してください。
