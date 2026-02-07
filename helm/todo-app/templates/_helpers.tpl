{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-app.backend.labels" -}}
{{ include "todo-app.labels" . }}
app: backend
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-app.frontend.labels" -}}
{{ include "todo-app.labels" . }}
app: frontend
{{- end }}
