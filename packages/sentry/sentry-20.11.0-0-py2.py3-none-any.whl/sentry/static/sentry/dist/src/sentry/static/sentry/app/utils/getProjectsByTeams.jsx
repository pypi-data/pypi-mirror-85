export default function getProjectsByTeams(teams, projects, isSuperuser) {
    if (isSuperuser === void 0) { isSuperuser = false; }
    var projectsByTeam = {};
    var teamlessProjects = [];
    var usersTeams = new Set(teams.filter(function (team) { return team.isMember; }).map(function (team) { return team.slug; }));
    if (usersTeams.size === 0 && isSuperuser) {
        usersTeams = new Set(teams.map(function (team) { return team.slug; }));
    }
    projects.forEach(function (project) {
        if (!project.teams.length && project.isMember) {
            teamlessProjects.push(project);
        }
        else {
            project.teams.forEach(function (team) {
                if (!usersTeams.has(team.slug)) {
                    return;
                }
                if (!projectsByTeam.hasOwnProperty(team.slug)) {
                    projectsByTeam[team.slug] = [];
                }
                projectsByTeam[team.slug].push(project);
            });
        }
    });
    return { projectsByTeam: projectsByTeam, teamlessProjects: teamlessProjects };
}
//# sourceMappingURL=getProjectsByTeams.jsx.map