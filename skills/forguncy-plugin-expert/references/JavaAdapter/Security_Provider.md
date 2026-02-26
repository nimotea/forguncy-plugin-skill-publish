# Security Provider

## JavaSecurityProvider

# Java安全提供程序

## Content

* [Java安全提供程序快速入门](/solutions/huozige/help/docs/java-adapter/java-security-provider/quick-start)
* [安装Java安全提供程序](/solutions/huozige/help/docs/java-adapter/java-security-provider/install)
* [Java安全提供程序主要概念](/solutions/huozige/help/docs/java-adapter/java-security-provider/Main-Concepts)
* [示例：Java 钉钉 安全提供程序](/solutions/huozige/help/docs/java-adapter/java-security-provider/dingding)

---

## Dingding

# 示例：Java 钉钉 安全提供程序

## Content

<span style="color: rgb(23, 43, 77); font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Fira Sans, Droid Sans, Helvetica Neue, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: -0.08px; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;">为了更好地与第三方系统对接，这里提供Java 钉钉安全提供程序的核心代码。</span>

```auto
package org.example;

import lombok.Data;

@Data
public class Config {
    private String appkey;
    private String secret;
    private String agentId;
    private String appId;
    private String appSecret;
}
auto
package org.example;

import com.dingtalk.api.DefaultDingTalkClient;
import com.dingtalk.api.DingTalkClient;
import com.dingtalk.api.request.*;
import com.dingtalk.api.response.*;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.json.JsonReadFeature;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.MapperFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.grapecity.forguncy.LoggerContext;
import com.grapecity.forguncy.securityprovider.*;
import com.grapecity.forguncy.securityprovider.settings.PasswordEditor;
import com.grapecity.forguncy.securityprovider.settings.SecurityProviderSettings;
import lombok.SneakyThrows;

import java.io.File;
import java.io.FileWriter;
import java.net.ContentHandler;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class DingTalkSecurityProvider implements ISecurityProvider, ISupportSettings, IOpenIdSecurityProvider {
    static String lastAccessToken;
    static Date lastAccessTokenTime;
    static String mobileCheck = "android|(android|bb\\d+|meego).+mobile|avantgo|bada/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)/|plucker|pocket|psp|series([46])0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino";
    static String mobileVersionCheck = "1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br([ev])w|bumb|bw-([nu])|c55/|capi|ccwa|cdm-|cell|chtm|cldc|cmd-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc-s|devi|dica|dmob|do([cp])o|ds(12|-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly([-_])|g1 u|g560|gene|gf-5|g-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd-([mpt])|hei-|hi(pt|ta)|hp( i|ip)|hs-c|ht(c([- _agpst])|tp)|hu(aw|tc)|i-(20|go|ma)|i230|iac([ \\-/])|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja([tv])a|jbro|jemu|jigs|kddi|keji|kgt([ /])|klon|kpt |kwc-|kyo([ck])|le(no|xi)|lg( g|/([klu])|50|54|-[a-w])|libw|lynx|m1-w|m3ga|m50/|ma(te|ui|xo)|mc(01|21|ca)|m-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t([- ov])|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30([02])|n50([025])|n7(0([01])|10)|ne(([cm])-|on|tf|wf|wg|wt)|nok([6i])|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan([adt])|pdxg|pg(13|-([1-8]|c))|phil|pire|pl(ay|uc)|pn-2|po(ck|rt|se)|prox|psio|pt-g|qa-a|qc(07|12|21|32|60|-[2-7]|i-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55/|sa(ge|ma|mm|ms|ny|va)|sc(01|h-|oo|p-)|sdk/|se(c([-01])|47|mc|nd|ri)|sgh-|shar|sie([-m])|sk-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h-|v-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl-|tdg-|tel([im])|tim-|t-mo|to(pl|sh)|ts(70|m-|m3|m5)|tx-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c([- ])|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas-|your|zeto|zte-";

    @SneakyThrows
    private Config loadConfig() {
        String path = new File(this.getClass().getProtectionDomain().getCodeSource().getLocation().getPath()).getParent() + File.separator + "config.json";
        File file = new File(path);
        ObjectMapper objectMapper = JsonMapper.builder()
                .enable(JsonReadFeature.ALLOW_BACKSLASH_ESCAPING_ANY_CHARACTER)
                .enable(MapperFeature.ACCEPT_CASE_INSENSITIVE_PROPERTIES)
                .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
                .enable(JsonParser.Feature.ALLOW_COMMENTS).build();
        return objectMapper.readValue(file, Config.class);
    }

    @SneakyThrows
    private String getAccessToken() {
        if (lastAccessToken != null && !lastAccessToken.isEmpty()) {
            if (System.currentTimeMillis() < lastAccessTokenTime.getTime()) {
                return lastAccessToken;
            }
        }
        String result = "";
        try {
            var config = loadConfig();
            DingTalkClient client = new DefaultDingTalkClient("https://oapi.dingtalk.com/gettoken");
            OapiGettokenRequest request = new OapiGettokenRequest();
            assert config != null;
            request.setAppkey(config.getAppkey());
            request.setAppsecret(config.getSecret());
            request.setHttpMethod("GET");
            OapiGettokenResponse response = client.execute(request);
            result = response.getAccessToken();
            lastAccessToken = result;
            long expires = response.getExpiresIn() * 1000;
            lastAccessTokenTime = new Date(expires);
            return lastAccessToken;
        } catch (Exception e) {
            throw new Exception("GetAccessToken Failed" + result, e);
        }
    }

    @Override
    public UserInformations getUserInformations() {
        Config config = loadConfig();
        if (config == null) {
            return null;
        }
        if (config.getAppkey() == null || config.getAppkey().isEmpty()) {
            return null;
        }
        return findUserInformations();
    }

    private UserInformations findUserInformations() {
        UserInformations userInformations = new UserInformations();
        ArrayList<OapiDepartmentListResponse.Department> departments = getDepartmentList();
        HashMap<Long, OapiDepartmentListResponse.Department> departmentDic = departments.stream().collect(HashMap::new, (m, v) -> m.put(v.getId(), v), HashMap::putAll);
        List<Long> rootDepartmentIds = departments.stream().filter(i -> !departmentDic.containsKey(i.getParentid()))
                .map(OapiDepartmentListResponse.Department::getId).toList();
        List<OapiRoleListResponse.OpenRole> roles = getRoles();
        HashMap<Long, OapiRoleListResponse.OpenRole> roleDic = roles.stream().collect(HashMap::new, (m, v) -> m.put(v.getId(), v), HashMap::putAll);
        HashMap<Long, com.grapecity.forguncy.securityprovider.Role> fRoleDic = new HashMap<>();
        for (var entry : roleDic.entrySet()) {
            fRoleDic.put(entry.getKey(), getForguncyRole(entry.getValue()));
        }
        List<OapiV2UserGetResponse.UserGetResponse> users = getUsers(departments);
        HashMap<String, OapiV2UserGetResponse.UserGetResponse> userDic = users.stream().collect(HashMap::new, (m, v) -> m.put(v.getUserid(), v), HashMap::putAll);
        var fUserDic = new HashMap<String, User>();
        for (var entry : userDic.entrySet()) {
            fUserDic.put(entry.getKey(), getForguncyUser(entry.getValue(), userDic));
        }
        addUsersToRoles(userDic, fUserDic, fRoleDic);
        HashMap<Long, Organization> fOrganizationDic = addDepartmentAndUsers(userInformations, departmentDic, userDic, fUserDic);
        for (var rootDepartmentId : rootDepartmentIds) {
            userInformations.getOrganizations().add(fOrganizationDic.get(rootDepartmentId));
        }
        addRoles(userInformations, new ArrayList<>(fRoleDic.values()));
        return userInformations;
    }

    private void addRoles(UserInformations userInfo, List<Role> roles) {
        for (var role : roles) {
            userInfo.getRoles().add(role);
        }
    }

    private HashMap<Long, Organization> addDepartmentAndUsers(UserInformations userInfo, HashMap<Long, OapiDepartmentListResponse.Department> departmentDic,
                                                              HashMap<String, OapiV2UserGetResponse.UserGetResponse> userDic, HashMap<String, User> fUserDic) {
        var fOrganizationDic = new HashMap<Long, Organization>();
        for (var entry : departmentDic.entrySet()) {
            fOrganizationDic.put(entry.getKey(), getForguncyOrganization(entry.getValue()));
        }
        for (var department : departmentDic.entrySet()) {
            if (fOrganizationDic.containsKey(department.getValue().getParentid())) {
                fOrganizationDic.get(department.getValue().getParentid()).getSubOrganizations().add(fOrganizationDic.get(department.getValue().getId()));
            }
        }
        for (var entry : fUserDic.entrySet()) {
            userInfo.getUsers().add(entry.getValue());
            OapiV2UserGetResponse.UserGetResponse userGetResponse = userDic.get(entry.getKey());
            if (userGetResponse.getDeptIdList() != null && !userGetResponse.getDeptIdList().isEmpty()) {
                for (var departmentId : userGetResponse.getDeptIdList()) {
                    if (fOrganizationDic.containsKey(departmentId)) {
                        boolean isOrgLeader = userGetResponse.getLeaderInDept().stream().anyMatch(x -> x.getLeader() && x.getDeptId().equals(departmentId));
                        OrganizationMember organizationMember = new OrganizationMember();
                        organizationMember.setUser(entry.getValue());
                        organizationMember.setIsLeader(isOrgLeader);
                        if (isOrgLeader) {
                            Role role = new Role();
                            role.setName("主管");
                            organizationMember.setOrganizationRoles(List.of(role));
                        }
                        fOrganizationDic.get(departmentId).getMembers().add(organizationMember);
                    }
                }
            }
        }
        return fOrganizationDic;
    }

    private void addUsersToRoles(HashMap<String, OapiV2UserGetResponse.UserGetResponse> userDic, HashMap<String, User> fUserDic, HashMap<Long, com.grapecity.forguncy.securityprovider.Role> fRoleDic) {
        for (var entry : userDic.entrySet()) {
            var user = entry.getValue();
            if (user.getRoleList() == null) {
                continue;
            }
            for (var role : user.getRoleList()) {
                Long roleId = role.getId();
                if (fRoleDic.containsKey(roleId) && fUserDic.containsKey(entry.getKey())) {
                    fRoleDic.get(roleId).getUsers().add(fUserDic.get(entry.getKey()));
                }
            }
        }
    }

    @SneakyThrows
    private List<OapiV2UserGetResponse.UserGetResponse> getUsers(ArrayList<OapiDepartmentListResponse.Department> departments) {
        String accessToken = getAccessToken();
        if (accessToken == null || accessToken.isEmpty()) {
            return new ArrayList<>();
        }
        ArrayList<OapiV2UserGetResponse.UserGetResponse> users = new ArrayList<>();
        var userIds = new HashSet<String>();
        for (var department : departments) {
            DingTalkClient dingTalkClient = new DefaultDingTalkClient("https://oapi.dingtalk.com/topapi/user/listid");
            OapiUserListidRequest oapiUserListidRequest = new OapiUserListidRequest();
            oapiUserListidRequest.setDeptId(department.getId());
            OapiUserListidResponse oapiUserListidResponse = dingTalkClient.execute(oapiUserListidRequest, getAccessToken());
            userIds.addAll(oapiUserListidResponse.getResult().getUseridList());
        }
        for (var key : userIds) {
            DingTalkClient dingTalkClient = new DefaultDingTalkClient("https://oapi.dingtalk.com/topapi/v2/user/get");
            OapiV2UserGetRequest req = new OapiV2UserGetRequest();
            req.setUserid(key);
            req.setLanguage("zh_CN");
            OapiV2UserGetResponse rsp = dingTalkClient.execute(req, getAccessToken());
            users.add(rsp.getResult());
        }
        return users;
    }

    @SneakyThrows
    private List<OapiRoleListResponse.OpenRole> getRoles() {
        String accessToken = getAccessToken();
        ArrayList<OapiRoleListResponse.OpenRole> roles = new ArrayList<>();
        if (accessToken == null || accessToken.isEmpty()) {
            return roles;
        }
        long offset = 0;
        long size = 200;
        var result = new ArrayList<OapiRoleListResponse.OpenRoleGroup>();
        while (true) {
            DingTalkClient client = new DefaultDingTalkClient("https://oapi.dingtalk.com/topapi/role/list");
            OapiRoleListRequest req = new OapiRoleListRequest();
            req.setSize(size);
            req.setOffset(offset);
            OapiRoleListResponse rsp = client.execute(req, accessToken);

            if (rsp.getErrcode() != 0) {
                throw new Exception("GetRoles Failed" + rsp.getBody());
            }
            result.addAll(rsp.getResult().getList());
            if (rsp.getResult().getHasMore()) {
                offset += size;
            } else {
                break;
            }
        }
        for (var roleGroup : result) {
            roles.addAll(roleGroup.getRoles());
        }
        return roles;
    }

    @SneakyThrows
    private ArrayList<OapiDepartmentListResponse.Department> getDepartmentList() {
        ArrayList<OapiDepartmentListResponse.Department> results = new ArrayList<>();
        String accessToken = getAccessToken();
        if (accessToken == null || accessToken.isEmpty()) {
            return results;
        }
        var authedDept = getAuthorizedDepartmentIds();
        for (Long aLong : authedDept) {
            List<OapiV2DepartmentListsubResponse.DeptBaseResponse> departmentAndChildren = getDepartmentAndChildren(aLong);
            List<OapiDepartmentListResponse.Department> departmentList = departmentAndChildren.stream().map(item -> {
                OapiDepartmentListResponse.Department department = new OapiDepartmentListResponse.Department();
                department.setId(item.getDeptId());
                department.setName(item.getName());
                department.setParentid(item.getParentId());
                department.setAutoAddUser(item.getAutoAddUser());
                department.setCreateDeptGroup(item.getCreateDeptGroup());
                return department;
            }).toList();
            results.addAll(departmentList);
        }
        HashSet<String> set = new HashSet<>();
        return (ArrayList<OapiDepartmentListResponse.Department>) results.stream().filter(item -> set.add(item.getId() + ""))
                .collect(Collectors.toList());
    }

    @SneakyThrows
    private List<OapiV2DepartmentListsubResponse.DeptBaseResponse> getDepartmentAndChildren(Long id) {
        var results = new ArrayList<OapiV2DepartmentListsubResponse.DeptBaseResponse>();
        String accessToken = getAccessToken();
        if (accessToken == null || accessToken.isEmpty()) {
            return results;
        }
        DingTalkClient client = new DefaultDingTalkClient("https://oapi.dingtalk.com/topapi/v2/department/get");
        OapiV2DepartmentGetRequest req = new OapiV2DepartmentGetRequest();
        req.setDeptId(id);
        req.setLanguage("zh_CN");
        OapiV2DepartmentGetResponse rsp = client.execute(req, accessToken);
        OapiV2DepartmentListsubResponse.DeptBaseResponse deptBaseResponse = new OapiV2DepartmentListsubResponse.DeptBaseResponse();
        deptBaseResponse.setDeptId(rsp.getResult().getDeptId());
        deptBaseResponse.setName(rsp.getResult().getName());
        deptBaseResponse.setParentId(rsp.getResult().getParentId());
        deptBaseResponse.setAutoAddUser(rsp.getResult().getAutoAddUser());
        deptBaseResponse.setCreateDeptGroup(rsp.getResult().getCreateDeptGroup());
        results.add(deptBaseResponse);

        Deque<Long> departmentQueue = new LinkedList<>();
        departmentQueue.add(rsp.getResult().getDeptId());
        while (!departmentQueue.isEmpty()) {
            Long departmentId = departmentQueue.poll();
            DingTalkClient client1 = new DefaultDingTalkClient("https://oapi.dingtalk.com/topapi/v2/department/listsub");
            OapiV2DepartmentListsubRequest req1 = new OapiV2DepartmentListsubRequest();
            req1.setDeptId(departmentId);
            req1.setLanguage("zh_CN");
            OapiV2DepartmentListsubResponse rsp1 = client1.execute(req1, accessToken);
            results.addAll(rsp1.getResult());
            for (var item : rsp1.getResult()) {
                departmentQueue.add(item.getDeptId());
            }
        }
        return results;
    }

    @SneakyThrows
    private List<Long> getAuthorizedDepartmentIds() {
        String accessToken = getAccessToken();
        DingTalkClient client = new DefaultDingTalkClient("https://oapi.dingtalk.com/auth/scopes");
        OapiAuthScopesRequest req = new OapiAuthScopesRequest();
        req.setHttpMethod("GET");
        OapiAuthScopesResponse rsp = client.execute(req, accessToken);
        if (rsp.getErrcode() != 0) {
            throw new Exception("GetDepartmentList Failed" + req);
        }
        return rsp.getAuthOrgScopes().getAuthedDept();
    }

    @SneakyThrows
    @Override
    public User verifyUser(HashMap<String, String> properties) {
        String code = properties.get("code");
        Config config = loadConfig();
        DefaultDingTalkClient client = new DefaultDingTalkClient("https://oapi.dingtalk.com/sns/getuserinfo_bycode");
        OapiSnsGetuserinfoBycodeRequest req = new OapiSnsGetuserinfoBycodeRequest();
        req.setTmpAuthCode(code);
        OapiSnsGetuserinfoBycodeResponse response = client.execute(req, config.getAppId(), config.getAppSecret());
        if (response.getErrcode() != 0) {
            throw new Exception("VerifyUser Failed" + response.getBody());
        }
        if (response.getUserInfo() == null) {
            throw new Exception("VerifyUser Failed" + response.getBody());
        }
        return getUser(response);
    }

    private User getUser(OapiSnsGetuserinfoBycodeResponse response) throws Exception {
        DingTalkClient dingTalkClient = new DefaultDingTalkClient("https://oapi.dingtalk.com/topapi/user/getbyunionid");
        OapiUserGetbyunionidRequest oapiUserGetbyunionidRequest = new OapiUserGetbyunionidRequest();
        oapiUserGetbyunionidRequest.setUnionid(response.getUserInfo().getUnionid());
        OapiUserGetbyunionidResponse oapiUserGetbyunionidResponse = dingTalkClient.execute(oapiUserGetbyunionidRequest, getAccessToken());
        if (oapiUserGetbyunionidResponse.getErrcode() != 0) {
            throw new Exception("VerifyUser Failed" + oapiUserGetbyunionidResponse.getBody());
        }
        if (oapiUserGetbyunionidResponse.getResult() == null) {
            throw new Exception("VerifyUser Failed" + oapiUserGetbyunionidResponse.getBody());
        }
        User user = new User();
        user.setUserId(oapiUserGetbyunionidResponse.getResult().getUserid());
        return user;
    }

    @Override
    public String getName() {
        return "Java DingTalk Security Provider";
    }

    @Override
    public AuthenticationType getAuthenticationType() {
        return AuthenticationType.OpenId;
    }

    @Override
    public UserInformationStorageMode getUserInformationStorageMode() {
        return UserInformationStorageMode.InMemoryCache;
    }

    @Override
    public boolean getAllowLogout() {
        return false;
    }

    @Override
    public String getRedirectUrl(String redirectUri, String state, String userAgent) {
        if (!needRedirect(userAgent)) {
            return null;
        }
        Map<String, String> queryString = new HashMap<>();
        Config config = loadConfig();
        queryString.put("appid", config.getAppId());
        queryString.put("response_type", "code");
        queryString.put("scope", "snsapi_auth");
        queryString.put("state", state);
        queryString.put("redirect_uri", URLEncoder.encode(String.valueOf(redirectUri), StandardCharsets.UTF_8));

        StringBuilder str = new StringBuilder();
        for (Map.Entry<String, String> entry : queryString.entrySet()) {
            str.append(entry.getKey()).append("=").append(entry.getValue()).append("&");
        }
        if (!str.isEmpty()) {
            str.deleteCharAt(str.length() - 1);
        }
        return "https://oapi.dingtalk.com/connect/oauth2/sns_authorize?" + str;
    }

    private boolean needRedirect(String userAgent) {
        if (userAgent == null || userAgent.isEmpty()) {
            return true;
        }
        if (isMobile(userAgent)) {
            return true;
        }
        return userAgent.toLowerCase().contains("dingtalk");
    }

    private boolean isMobile(String userAgent) {
        if (userAgent == null || userAgent.isEmpty()) {
            return false;
        }
        if (userAgent.length() < 4) {
            return false;
        }
        Pattern mobileCheckPattern = Pattern.compile(mobileCheck, Pattern.CASE_INSENSITIVE | Pattern.MULTILINE);
        Pattern mobileVersionCheckPattern = Pattern.compile(mobileVersionCheck, Pattern.CASE_INSENSITIVE | Pattern.MULTILINE);
        return mobileCheckPattern.matcher(userAgent).find() || mobileVersionCheckPattern.matcher(userAgent.substring(0, 4)).find();
    }

    @Override
    public List<SecurityProviderSettings> getSettings() {
        Config config = loadConfig();
        ArrayList<SecurityProviderSettings> settings = new ArrayList<>();
        SecurityProviderSettings securityProviderSettings = new SecurityProviderSettings();
        securityProviderSettings.setName("AppKey");
        assert config != null;
        securityProviderSettings.setValue(config.getAppkey());
        settings.add(securityProviderSettings);

        securityProviderSettings = new SecurityProviderSettings();
        securityProviderSettings.setName("Secret");
        securityProviderSettings.setValue(config.getSecret());
        securityProviderSettings.setEditor(new PasswordEditor());
        settings.add(securityProviderSettings);

        securityProviderSettings = new SecurityProviderSettings();
        securityProviderSettings.setName("AppId");
        securityProviderSettings.setValue(config.getAppId());
        settings.add(securityProviderSettings);

        securityProviderSettings = new SecurityProviderSettings();
        securityProviderSettings.setName("AppSecret");
        securityProviderSettings.setValue(config.getAppSecret());
        securityProviderSettings.setEditor(new PasswordEditor());
        settings.add(securityProviderSettings);
        return settings;

    }

    @Override
    public void updateSetting(HashMap<String, Object> dictionary) {
        var config = loadConfig();
        assert config != null;
        if (dictionary.containsKey("AppKey")) {
            config.setAppkey(dictionary.get("AppKey") + "");
        }
        if (dictionary.containsKey("AppSecret")) {
            config.setAppSecret(dictionary.get("AppSecret") + "");
        }
        if (dictionary.containsKey("Secret")) {
            config.setSecret(dictionary.get("Secret") + "");
        }
        if (dictionary.containsKey("AppId")) {
            config.setAppId(dictionary.get("AppId") + "");
        }
        saveConfig(config);
    }

    @SneakyThrows
    private void saveConfig(Config config) {
        lastAccessToken = null;
        var configPath = new File(this.getClass().getProtectionDomain().getCodeSource().getLocation().getPath()).getParent() + File.separator + "config.json";
        File file = new File(configPath);
        if (!file.canWrite() && !file.setWritable(true)) {
            throw new Exception("set file writable failed");
        }
        try (FileWriter fileWriter = new FileWriter(file)) {
            fileWriter.write(new ObjectMapper().writeValueAsString(config));
        }
    }

    private com.grapecity.forguncy.securityprovider.Role getForguncyRole(OapiRoleListResponse.OpenRole value) {
        var role = new com.grapecity.forguncy.securityprovider.Role();
        role.setName(value.getName());
        return role;
    }

    private Organization getForguncyOrganization(OapiDepartmentListResponse.Department value) {
        var organization = new Organization();
        organization.setName(value.getName());
        organization.setOrganizationLevel("部门");
        return organization;
    }

    private User getForguncyUser(OapiV2UserGetResponse.UserGetResponse value, HashMap<String, OapiV2UserGetResponse.UserGetResponse> userHashMap) {
        var forguncyUser = new User();
        forguncyUser.setUserId(value.getUserid());
        forguncyUser.setEmail(value.getEmail());
        forguncyUser.setFullName(value.getName());
        forguncyUser.getProperties().put("手机号码", value.getMobile());
        forguncyUser.getProperties().put("职务", value.getTitle());
        forguncyUser.getProperties().put("分号", value.getTelephone());
        forguncyUser.getProperties().put("工作地点", value.getWorkPlace());
        forguncyUser.getProperties().put("备注", value.getRemark());
        forguncyUser.getProperties().put("是否为管理员", value.getAdmin());
        forguncyUser.getProperties().put("是否为老板", value.getBoss());
        boolean isLeader = false;
        if (value.getLeaderInDept() != null) {
            isLeader = value.getLeaderInDept().stream().anyMatch(x -> x.getLeader() != null);
        }
        forguncyUser.getProperties().put("主管", isLeader);
        if (value.getManagerUserid() == null || userHashMap.containsKey(value.getManagerUserid())) {
            forguncyUser.getProperties().put("直属主管", null);
        } else {
            forguncyUser.getProperties().put("直属主管", userHashMap.get(value.getManagerUserid()).getName());
        }
        forguncyUser.getProperties().put("激活", value.getActive());
        forguncyUser.getProperties().put("工号", value.getJobNumber());
        forguncyUser.getProperties().put("钉钉unionid", value.getUnionid());
        return forguncyUser;
    }
}
```

代码中的config.json放到如下位置：

从代码中可知：

* 钉钉集成使用了 OpenId 的认证模式，因此安全提供程序需要实现 IOpenIdSecurityProvider 接口返回 OAuth 登录地址。
* 钉钉的 OAuth 接口需要大量的认证相关的参数，因此需要实现 ISupportSettings 在管理控制台配置相关参数。
* 为了提供用户认证使用到了 verifyUser 接口。
* 安全提供程序只有两个任务：1. 请求钉钉的接口获取用户数据； 2. 登录时通过请求参数验证用户是否登录。