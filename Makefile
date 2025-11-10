# ==========================================================
# 🔖 Versioning & Auto Changelog (ENG/ESP)
# ==========================================================

# Version file + date
VERSION_FILE := VERSION
VERSION := $(shell cat $(VERSION_FILE) 2>/dev/null || echo "1.0.0")
DATE := $(shell date +'%Y-%m-%d')

# Último tag (si existe) para delimitar rango de commits
LAST_TAG := $(shell git describe --tags --abbrev=0 2>/dev/null)
GIT_RANGE := $(if $(LAST_TAG),$(LAST_TAG)..HEAD,HEAD)

# ---------- Bumps semánticos ----------
define BUMP_VERSION
	@old=$$(cat $(VERSION_FILE) 2>/dev/null || echo "1.0.0"); \
	IFS=. read -r major minor patch <<< $$old; \
	case $(1) in \
		major) major=$$((major+1)); minor=0; patch=0 ;; \
		minor) minor=$$((minor+1)); patch=0 ;; \
		patch) patch=$$((patch+1)) ;; \
	esac; \
	new_version="$$major.$$minor.$$patch"; \
	echo "$$new_version" > $(VERSION_FILE); \
	echo "🔢 Bumped version → $$new_version"
endef

bump-major: ; $(call BUMP_VERSION,major)
bump-minor: ; $(call BUMP_VERSION,minor)
bump-patch: ; $(call BUMP_VERSION,patch)

# ---------- Changelog simple (plantilla manual) ----------
changelog:
	@echo "📝 Updating CHANGELOG.md..."
	@echo "" >> CHANGELOG.md
	@echo "## [$(VERSION)] - $(DATE)" >> CHANGELOG.md
	@echo "### 🚀 Changes" >> CHANGELOG.md
	@echo "" >> CHANGELOG.md
	@echo "- _Describe new features, fixes, or enhancements here._" >> CHANGELOG.md
	@echo "" >> CHANGELOG.md
	@echo "✅ Changelog updated for version $(VERSION)."

# ---------- Changelog automático desde commits ----------
# Usa Conventional Commits: feat:, fix:, chore:, refactor:, perf:, test:, docs:, build:, ci:
changelog-auto:
	@echo "🧾 Generating CHANGELOG from commits ($(if $(LAST_TAG),since $(LAST_TAG),from start)))"
	@tmp=$$(mktemp); \
	echo "## [$(VERSION)] - $(DATE)" > $$tmp; \
	echo "" >> $$tmp; \
	echo "### Changes $(if $(LAST_TAG),since $(LAST_TAG),from start)" >> $$tmp; \
	echo "" >> $$tmp; \
	range="$(GIT_RANGE)"; \
	log_cmd="git log --no-merges --pretty=format:%s|%h|%an $$range"; \
	commits=$$($$log_cmd || true); \
	gen_section() { \
	  title="$$1"; prefix="$$2"; \
	  lines=$$(printf "%s\n" "$$commits" | grep -Eim 999 "^$$prefix:" || true); \
	  if [ -n "$$lines" ]; then \
	    echo "#### $$title" >> $$tmp; \
	    printf "%s\n" "$$lines" \
	      | sed -E 's/^[^:]+:\s*//; s/\|/ | /g' \
	      | awk -F' \\| ' '{printf "- %s (%s) — %s\n", $$1, $$2, $$3}' >> $$tmp; \
	    echo "" >> $$tmp; \
	  fi; \
	}; \
	gen_section "✨ Features" "feat"; \
	gen_section "🐞 Fixes" "fix"; \
	gen_section "🧹 Chores" "chore"; \
	gen_section "🧰 Refactors" "refactor"; \
	gen_section "⚡ Performance" "perf"; \
	gen_section "🧪 Tests" "test"; \
	gen_section "📝 Docs" "docs?"; \
	gen_section "🏗 Build/CI" "build|ci"; \
	others=$$(printf "%s\n" "$$commits" | grep -Ev '^(feat|fix|chore|refactor|perf|test|docs?|build|ci):' || true); \
	if [ -n "$$others" ]; then \
	  echo "#### 📦 Other" >> $$tmp; \
	  printf "%s\n" "$$others" \
	    | sed -E 's/^[^:]+:\s*//; s/\|/ | /g' \
	    | awk -F' \\| ' '{printf "- %s (%s) — %s\n", $$1, $$2, $$3}' >> $$tmp; \
	  echo "" >> $$tmp; \
	fi; \
	touch CHANGELOG.md; \
	cat $$tmp CHANGELOG.md > CHANGELOG.md.new; mv CHANGELOG.md.new CHANGELOG.md; rm -f $$tmp; \
	echo "✅ CHANGELOG.md updated."

# ---------- Release helpers ----------
release:
	@ver=$$(cat $(VERSION_FILE)); \
	echo "🏷️ Releasing version $$ver"; \
	git add $(VERSION_FILE) CHANGELOG.md; \
	git commit -m "chore(release): version $$ver" || true; \
	git tag -a "v$$ver" -m "Release v$$ver" || true; \
	git push origin HEAD --tags; \
	echo "✅ Release $$ver pushed."

release-patch: bump-patch changelog-auto release
release-minor: bump-minor changelog-auto release
release-major: bump-major changelog-auto release

# ---------- (Opcional) Verificación de Conventional Commits en HEAD~20 ----------
conventional-check:
	@echo "🔎 Checking last 20 commit messages (Conventional Commits)"; \
	if git log -n 20 --pretty=format:%s | \
	   grep -Ev '^(feat|fix|chore|refactor|perf|test|docs?|build|ci)(\(.+\))?: .+' >/dev/null; then \
		echo "⚠️  Some commits don't match Conventional Commits. Consider squashing or editing."; \
		git log -n 20 --pretty=format:'- %h %s' | sed -E 's/^/- /'; \
	else \
		echo "✅ All good!"; \
	fi