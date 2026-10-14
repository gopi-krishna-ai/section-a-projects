document.addEventListener("DOMContentLoaded", () => {
    const subjectForm = document.getElementById("subject-form");
    const settingsForm = document.getElementById("settings-form");
    const formError = document.getElementById("form-error");
    const subjectsList = document.getElementById("subjects-list");
    const recommendationsList = document.getElementById("recommendations-list");
    const scheduleGrid = document.getElementById("schedule-grid");
    const analyticsChart = document.getElementById("analytics-chart");
    const summaryStats = document.getElementById("summary-stats");

    let toastTimer;

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    function priorityColor(priority) {
        return { High: "var(--high)", Medium: "var(--medium)", Low: "var(--low)" }[priority] || "var(--accent)";
    }

    function todayIso() {
        return new Date().toISOString().slice(0, 10);
    }

    function showToast(message) {
        let toast = document.getElementById("toast");
        if (!toast) {
            toast = document.createElement("div");
            toast.id = "toast";
            toast.className = "toast";
            document.body.appendChild(toast);
        }
        toast.textContent = message;
        toast.classList.add("show");
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.classList.remove("show"), 2200);
    }

    async function api(url, method, body) {
        const res = await fetch(url, {
            method,
            headers: body ? { "Content-Type": "application/json" } : undefined,
            body: body ? JSON.stringify(body) : undefined,
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Something went wrong.");
        return data;
    }

    function renderSummary(view) {
        const totalSubjects = view.subjects.length;
        const completedSubjects = view.subjects.filter((s) => s.syllabus_complete).length;
        const highPriority = view.subjects.filter((s) => s.priority === "High").length;
        const totalProgress = totalSubjects
            ? Math.round(view.subjects.reduce((sum, s) => sum + s.completion_pct, 0) / totalSubjects)
            : 0;
        const sessions = view.schedule.reduce((sum, day) => sum + day.sessions.length, 0);
        const hours = (sessions * 25 / 60).toFixed(1);

        summaryStats.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">Subjects</div>
                <div class="stat-value">${totalSubjects}</div>
                <div class="stat-note">${completedSubjects} syllabus-complete</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg. Progress</div>
                <div class="stat-value">${totalProgress}%</div>
                <div class="stat-note">Across all active subjects</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">High Priority</div>
                <div class="stat-value">${highPriority}</div>
                <div class="stat-note">Subjects needing attention</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Upcoming Study</div>
                <div class="stat-value">${hours}h</div>
                <div class="stat-note">Sessions remaining in view</div>
            </div>
        `;
    }

    function renderSubjects(view) {
        subjectsList.innerHTML = "";
        if (!view.subjects.length) {
            subjectsList.innerHTML = '<p class="empty-state">No subjects yet — add one above to build your personalized plan.</p>';
            return;
        }

        view.subjects.forEach((s) => {
            const card = document.createElement("div");
            card.className = "subject-card";
            card.innerHTML = `
                <div class="subject-info">
                    <div class="subject-name">${escapeHtml(s.name)}</div>
                    <div class="subject-meta">
                        ${s.exam_passed ? "Exam date passed" : `${s.days_to_exam} day(s) to exam`}
                        &middot; ${s.completed_topics}/${s.total_topics} topics
                        &middot; difficulty ${s.difficulty}/5
                        &middot; weightage ${s.weightage}/5
                    </div>
                </div>
                <span class="badge ${s.priority}">${s.priority} &middot; ${s.urgency_score}/100</span>
                <div class="subject-footer">
                    <div class="progress-bar-bg" title="${s.completion_pct}% complete">
                        <div class="progress-bar-fill" style="width:${s.completion_pct}%"></div>
                    </div>
                    <span class="subject-meta">${s.completion_pct}% complete</span>
                </div>
                <button class="delete-btn" data-name="${escapeHtml(s.name)}">Remove subject</button>
            `;
            subjectsList.appendChild(card);
        });

        subjectsList.querySelectorAll(".delete-btn").forEach((btn) => {
            btn.addEventListener("click", async () => {
                if (!confirm(`Remove "${btn.dataset.name}" from the planner?`)) return;
                try {
                    const view = await api(`/subjects/${encodeURIComponent(btn.dataset.name)}`, "DELETE");
                    renderAll(view);
                    showToast("Subject removed");
                } catch (err) {
                    formError.textContent = err.message;
                }
            });
        });
    }

    function renderRecommendations(view) {
        recommendationsList.innerHTML = "";
        view.recommendations.forEach((text) => {
            const li = document.createElement("li");
            li.textContent = text;
            recommendationsList.appendChild(li);
        });
    }

    function renderSchedule(view) {
        scheduleGrid.innerHTML = "";
        const today = todayIso();

        view.schedule.forEach((day) => {
            const col = document.createElement("div");
            col.className = `day-column${day.date === today ? " today-column" : ""}`;

            const dateLabel = new Date(day.date + "T00:00:00").toLocaleDateString(undefined, {
                month: "short",
                day: "numeric",
            });
            col.innerHTML = `
                <div class="day-header">${day.weekday}${day.date === today ? ' <span class="today-label">· Today</span>' : ""}</div>
                <div class="day-subheader">${dateLabel}</div>
            `;

            if (!day.sessions.length) {
                const rest = document.createElement("div");
                rest.className = "empty-state";
                rest.textContent = day.date === today ? "All planned sessions are handled." : "No sessions";
                col.appendChild(rest);
            }

                day.sessions.forEach((session) => {
                const card = document.createElement("div");
                card.className = "session-card";
                card.style.borderLeft = `4px solid ${priorityColor(session.priority)}`;
                
                const topicHtml = session.topic ? `<div style="font-size: 0.9em; color: #4a5568; margin-top: 4px; font-weight: 500;">&#128214; ${escapeHtml(session.topic)}</div>` : '';

                card.innerHTML = `
                    <div class="session-top">
                        <span class="session-subject">${escapeHtml(session.subject)}</span>
                        <span class="badge ${session.priority}">${session.priority}</span>
                    </div>
                    ${topicHtml}
                    <div style="margin-top: 8px;">${session.duration_minutes} min study + ${session.break_minutes} min break</div>
                    <div class="session-actions">
                        <button class="complete-btn" data-subject="${escapeHtml(session.subject)}" data-date="${day.date}">&#10003; Done</button>
                        <button class="missed-btn" data-subject="${escapeHtml(session.subject)}" data-date="${day.date}">&#10007; Missed</button>
                    </div>
                `;
                col.appendChild(card);
            });

            scheduleGrid.appendChild(col);
        });

        scheduleGrid.querySelectorAll(".session-actions button").forEach((btn) => {
            btn.addEventListener("click", async () => {
                const action = btn.classList.contains("complete-btn") ? "complete" : "missed";
                btn.disabled = true;
                formError.textContent = "";

                try {
                    const view = await api(`/session/${action}`, "POST", {
                        subject: btn.dataset.subject,
                        session_date: btn.dataset.date,
                    });
                    renderAll(view);
                    showToast(action === "complete" ? "Session completed ✓" : "Session marked as missed");
                } catch (err) {
                    btn.disabled = false;
                    formError.textContent = err.message;
                }
            });
        });
    }

    function renderAnalytics(view) {
        analyticsChart.innerHTML = "";
        if (!view.analytics.subjects.length) {
            analyticsChart.innerHTML = '<p class="empty-state">Add subjects to see progress analytics.</p>';
            return;
        }

        view.analytics.subjects.forEach((s) => {
            const row = document.createElement("div");
            row.className = "analytics-row";
            row.innerHTML = `
                <span class="analytics-label" title="${escapeHtml(s.name)}">${escapeHtml(s.name)}</span>
                <div class="analytics-bar-bg">
                    <div class="analytics-bar-fill" style="width:${s.completion_pct}%; background:${priorityColor(s.priority)}"></div>
                </div>
                <span class="analytics-pct">${s.completion_pct}%</span>
            `;
            analyticsChart.appendChild(row);
        });

        const missedNote = document.createElement("p");
        missedNote.className = "map-note";
        missedNote.textContent = `${view.analytics.missed_sessions_this_week} missed session(s) logged this week.`;
        analyticsChart.appendChild(missedNote);
    }

    function renderAll(view) {
        renderSummary(view);
        renderSubjects(view);
        renderRecommendations(view);
        renderSchedule(view);
        renderAnalytics(view);
    }

    // Prevent impossible topic values and improve the input experience.
    document.getElementById("total_topics").addEventListener("input", () => {
        const total = Number(document.getElementById("total_topics").value || 0);
        const completed = document.getElementById("completed_topics");
        completed.max = total > 0 ? total : "";
        if (Number(completed.value) > total) completed.value = total;
    });

    document.getElementById("exam_date").min = todayIso();

    subjectForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.textContent = "";

        const payload = {
            name: document.getElementById("name").value.trim(),
            exam_date: document.getElementById("exam_date").value,
            total_topics: document.getElementById("total_topics").value,
            completed_topics: document.getElementById("completed_topics").value,
            difficulty: document.getElementById("difficulty").value,
            weightage: document.getElementById("weightage").value,
        };

        try {
            const view = await api("/subjects", "POST", payload);
            renderAll(view);
            subjectForm.reset();
            document.getElementById("difficulty").value = "3";
            document.getElementById("weightage").value = "3";
            showToast("Subject added and schedule updated");
            window.scrollTo({ top: 0, behavior: "smooth" });
        } catch (err) {
            formError.textContent = err.message;
        }
    });

    settingsForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.textContent = "";
        try {
            const view = await api("/settings", "POST", {
                daily_hours: document.getElementById("daily_hours").value
            });
            renderAll(view);
            showToast("Daily study time updated");
        } catch (err) {
            formError.textContent = err.message;
        }
    });

    renderAll(INITIAL_VIEW);
});


    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const statusEl = document.getElementById('upload-status');
            statusEl.textContent = 'Uploading and extracting topics...';
            
            const formData = new FormData();
            formData.append('subject', document.getElementById('upload-subject').value);
            formData.append('file', document.getElementById('upload-file').files[0]);
            
            try {
                const res = await fetch('/upload_syllabus', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (res.ok) {
                    statusEl.textContent = 'Topics extracted and added to schedule!';
                    renderAll(data);
                    uploadForm.reset();
                } else {
                    statusEl.textContent = data.error || 'Upload failed.';
                }
            } catch (err) {
                statusEl.textContent = 'Network error.';
            }
        });
    }
